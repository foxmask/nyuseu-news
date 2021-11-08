# coding: utf-8
"""
   Nyuseu - 뉴스 - News - The Server
"""
import argparse
import asyncio
from html import escape
import json
import opml
import orm
import os
from rich.console import Console
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from nyuseu_server.models import Feeds, Folders  # noqa: E402

__author__ = 'FoxMaSk'
__all__ = ['dump', 'load']

console = Console()


async def dump(opml_resource):
    """
    export an OPML file
    """

    header = """
<opml version="1.0" encoding="UTF-8">
    <head>
        <title>Nyuseu subscriptions</title>
    </head>
    <body>
"""
    footer = """
    </body>
</opml>
"""
    if opml_resource.endswith('.opml') is False:
        console.print(f"the file you provided {opml_resource} does not have a valid file extension, expected .opml",
                      style="bold red")
    else:
        with open(opml_resource, "w+") as f:
            f.write(header)
            folders = await Folders.objects.all()
            for folder in folders:
                f.write(f'        <outline text="{folder.title}" title="{folder.title}">\n')
                feeds = await Feeds.objects.select_related("folder").filter(folder=folder.id).all()
                for feed in feeds:
                    line = f'           <outline type="rss" text="{feed.title}" title="{feed.title}" '
                    line += f'xmlUrl="{escape(feed.url)}" htmlUrl="{escape(feed.url)}"/>\n'
                    f.write(line)
                f.write('        </outline>\n')
            f.write(footer)

            console.print(f'Nyuseu - 뉴스 - News - The Server - Feeds Exported in file {opml_resource}', style="green")
        return json.dumps({'status': "opml file dumped"})


async def load(opml_resource):
    """
    import an OPML file
    """
    if opml_resource.endswith('.opml'):
        o_resource = opml.parse(opml_resource)
        for folder in o_resource:
            for feed in folder:
                print(folder.text, feed.text)
                # create the target folder if not exists
                try:
                    f = await Folders.objects.get(title=folder.text)
                except orm.exceptions.NoMatch:
                    f = await Folders.objects.create(title=folder.text)

                # create the target SourceFeeds source if not exists
                try:
                    await Feeds.objects.get(title=feed.text)
                except orm.exceptions.NoMatch:
                    await Feeds.objects.create(title=feed.text, url=feed.xmlUrl, folder=f)
        console.print('Nyuseu Server - 뉴스 - Feeds Loaded', style="green")
        return json.dumps({'status': "opml file loaded"})
    else:
        console.print(f"File {opml_resource} is not an OPML file", style="green")


# Bootstrap
if __name__ == '__main__':
    console.print('Nyuseu - 뉴스 - News - The Server - OPML Import/Export - Starlette powered', style="blue")
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="load or dump", type=str)
    parser.add_argument("opml_file", help="provide the path to the OPML file", type=str)
    args = parser.parse_args()
    if args.action == 'load':
        asyncio.run(load(args.opml_file))
    elif args.action == 'dump':
        asyncio.run(dump(args.opml_file))
    else:
        console.print("invalid arguments provided", style="magenta bold")
        console.print(parser.print_help())
