import argparse
import asyncio
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
__all__ = ['load']

console = Console()


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
    console.print('Nyuseu Server - 뉴스 - Feeds Reader Server - Starlette powered', style="blue")
    parser = argparse.ArgumentParser()
    parser.add_argument("opml_file", help="provide the path to the OPML file", type=str)
    args = parser.parse_args()
    asyncio.run(load(args.opml_file))
