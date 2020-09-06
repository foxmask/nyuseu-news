# coding: utf-8
"""
   뉴스 Engine
"""
# std lib
from __future__ import unicode_literals
import arrow
from bs4 import BeautifulSoup
import feedparser
import datetime
import logging.config
import os
from rich.console import Console
from starlette.config import Config
import sys
import time

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from nyuseu_server.models import Feeds, Articles  # noqa: E402
from nyuseu_server.rss import Rss  # noqa: E402

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

config = Config('.env')
console = Console()

__author__ = 'FoxMaSk'
__all__ = ['go']


def get_published(entry) -> datetime:
    """
    get the 'published' attribute
    :param entry:
    :return: datetime
    """
    published = None
    if hasattr(entry, 'published_parsed'):
        if entry.published_parsed is not None:
            published = datetime.datetime.utcfromtimestamp(time.mktime(entry.published_parsed))
    elif hasattr(entry, 'created_parsed'):
        if entry.created_parsed is not None:
            published = datetime.datetime.utcfromtimestamp(time.mktime(entry.created_parsed))
    elif hasattr(entry, 'updated_parsed'):
        if entry.updated_parsed is not None:
            published = datetime.datetime.utcfromtimestamp(time.mktime(entry.updated_parsed))
    return published


def _get_content(data, which_content):
    """
    check which content is present in the Feeds to return the right one
    :param data: feeds content
    :param which_content: one of content/summary_detail/description
    :return:
    """
    content = ''

    if data.get(which_content):
        if isinstance(data.get(which_content), feedparser.FeedParserDict):
            content = data.get(which_content)['value']
        elif not isinstance(data.get(which_content), str):
            if 'value' in data.get(which_content)[0]:
                content = data.get(which_content)[0].value
        else:
            content = data.get(which_content)
    return content


def revamped_images(content):
    """

    """
    soup = BeautifulSoup(content, 'html.parser')
    images = soup.find_all('img')
    if images:
        i = 0
        card_class = 'card-img-top'
        for image in images:
            if i > 0:
                card_class = 'card-img'
            image['class'] = card_class
            del image['height']
            del image['width']
            i += 1
        content = soup
    return content


def set_content(entry):
    """
    which content to return ?
    :param entry:
    :return: the body of the RSS data
    """
    content = _get_content(entry, 'content')

    if content == '':
        content = _get_content(entry, 'summary_detail')

    if content == '':
        if entry.get('description'):
            content = entry.get('description')

    image = get_image(entry, content)
    content = revamped_images(content)
    return content, image


def from_feed(entry):
    """

    """
    new_image = "<img src=\"{src}\" title=\"{title}\" class=\"card-img-top\" />"
    for link in entry.get('links'):
        if link['type'] in ('image/jpeg', 'image/png', 'image/jpg', 'image/gif') and link['rel'] == 'enclosure':
            new_image = new_image.format(src=link['href'], title=entry.title)
            return new_image
    if 'media_thumbnail' in entry:
        for link in entry.get('media_thumbnail'):
            new_image = new_image.format(src=link['url'], title=entry.title)
            return new_image
    return ''


def from_content(content):
    """

    """
    soup = BeautifulSoup(content, 'html.parser')
    new_image = ""
    if soup.find_all('img'):
        image = soup.find_all('img')[0]
        alt = image['alt'] if 'alt' in image else ''
        title = image['title'] if 'title' in image else ''
        new_image = "<img src=\"{src}\" alt=\"{alt}\" title=\"{title}\" class=\"card-img-top\" />"
        new_image = new_image.format(src=image['src'], alt=alt, title=title)
    return new_image


def get_image(entry, content):
    """

    """
    new_image = from_feed(entry)
    if new_image == '':
        new_image = from_content(content)

    return str(new_image)


async def go():
    """

    """
    console.print('Nyuseu Server Engine - 뉴스 - Feeds Reader Server - in progress', style="green")
    feeds = await Feeds.objects.all()
    for my_feeds in feeds:
        rss = Rss()
        console.print(f"Feeds {my_feeds.url}", style="magenta")
        feeds = await rss.get_data(**{'url_to_parse': my_feeds.url, 'bypass_bozo': config('BYPASS_BOZO')})
        now = arrow.utcnow().to(config('TIME_ZONE')).format('YYYY-MM-DDTHH:mm:ssZZ')
        date_grabbed = arrow.get(my_feeds.date_grabbed).format('YYYY-MM-DDTHH:mm:ssZZ')
        read_entries = 0
        created_entries = 0
        for entry in feeds.entries:
            read_entries += 1
            # entry.*_parsed may be None when the date in a RSS Feed is invalid
            # so will have the "now" date as default
            published = get_published(entry)
            if published:
                published = arrow.get(published).to(config('TIME_ZONE')).format('YYYY-MM-DDTHH:mm:ssZZ')
            # last triggered execution
            if published is not None and now >= published >= date_grabbed:
                content, image = set_content(entry)
                # add an article
                res = await Articles.objects.create(title=entry.title,
                                                    text=str(content),
                                                    image=str(image),
                                                    feeds=my_feeds,
                                                    source_url=entry.link,
                                                    read=False,
                                                    read_later=False)
                if res:
                    created_entries += 1
                    now = arrow.utcnow().to(config('TIME_ZONE')).format('YYYY-MM-DD HH:mm:ssZZ')
                    source_feeds = await Feeds.objects.get(id=my_feeds.id)
                    await source_feeds.update(date_grabbed=now)
                    console.print(f'Feeds {my_feeds.title} : {entry.title}', style="blue")

        if read_entries:
            console.print(f'{my_feeds.title}: Entries created {created_entries} / Read {read_entries}', style="magenta")
        else:
            console.print(f'{my_feeds.title}: no feeds read', style="blue")

    console.print('Nyuseu Server Engine - 뉴스 - Feeds Reader Server - Finished!', style="green")

# Bootstrap
if __name__ == '__main__':
    import asyncio
    asyncio.run(go())
