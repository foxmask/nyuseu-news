# coding: utf-8
"""
   뉴스 Engine
"""
# std lib
from __future__ import unicode_literals
import feedparser
import datetime
import logging.config
import os
import sys
import time
# external lib
import arrow
from starlette.config import Config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from nyuseu_server.models import Feeds, Articles
from nyuseu_server.rss import Rss

config = Config('.env')

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
    logger.debug(published)
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
    logger.debug(content)
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
    logger.debug(content)
    return content


async def go():
    """

    """
    logger.info('Nyuseu Server Engine - 뉴스 - Feeds Reader Server - in progress')
    feeds = await Feeds.objects.all()
    for my_feeds in feeds:
        rss = Rss()
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
                content = set_content(entry)
                res = await Articles.objects.create(title=entry.title, text=content, feeds=my_feeds)
                if res:
                    created_entries += 1
                    now = arrow.utcnow().to(config('TIME_ZONE')).format('YYYY-MM-DD HH:mm:ssZZ')
                    source_feeds = await Feeds.objects.get(id=my_feeds.id)
                    await source_feeds.update(date_grabbed=now)
                    logger.info(f'Feeds {my_feeds.title} : {entry.title}')

        if read_entries:
            logger.info(f'{my_feeds.title}: Entries created {created_entries} / Read {read_entries}')
        else:
            logger.info(f'{my_feeds.title}: no feeds read')

    logger.info('Nyuseu Server Engine - 뉴스 - Feeds Reader Server - Finished!')

# Bootstrap
if __name__ == '__main__':
    import asyncio
    asyncio.run(go())
