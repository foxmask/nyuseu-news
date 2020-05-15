import argparse
import asyncio
import json
import opml
import orm
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from nyuseu_server.models import SourceFeeds, Folders

__author__ = 'FoxMaSk'
__all__ = ['load']


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
                except orm.exceptions.NoMatch as e:
                    f = await Folders.objects.create(title=folder.text)

                # create the target SourceFeeds source if not exists
                try:
                    res = await SourceFeeds.objects.get(title=feed.text)
                except orm.exceptions.NoMatch as e:
                    res = await SourceFeeds.objects.create(title=feed.text,
                                                           url=feed.xmlUrl,
                                                           folder=f)
        print('Nyuseu Server - 뉴스 - Feeds Loaded')
        return json.dumps({'status': "opml file loaded"})
    else:
        print(f"File {opml_resource} is not an OPML file")

# Bootstrap
if __name__ == '__main__':
    print('Nyuseu Server - 뉴스 - Feeds Reader Server - Starlette powered')
    parser = argparse.ArgumentParser()
    parser.add_argument("opml_file", help="provide the path to the OPML file", type=str)
    args = parser.parse_args()
    asyncio.run(load(args.opml_file))
