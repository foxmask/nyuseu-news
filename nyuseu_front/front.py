# coding: utf-8
"""
   Nyuseu Front - 뉴스 - sauce starlette
"""
import httpx
import json
import logging
import os
# starlette
from starlette.applications import Starlette
from starlette.config import Config
from starlette.routing import Mount, Router, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import sys
# uvicorn
import uvicorn

from pprint import pprint
templates = Jinja2Templates(directory="templates")

# logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

# load configuration
settings = Config('.env')

main_app = Starlette()
main_app.debug = settings('NYUSEU_FRONT_DEBUG', default=False)
# call the back, not the server directly
NYUSEU_HOST = settings('NYUSEU_HOST', default='http://localhost')
NYUSEU_PORT = settings('NYUSEU_PORT', default='8002')


async def get_feeds_by_folders():
    """
    get all the folders
    ... and their feeds
    """
    folders = httpx.get(f'{NYUSEU_HOST}:{NYUSEU_PORT}/api/nyuseu/folders/')
    folders_and_feeds = []
    for folder in folders.json():
        folder_id = folder['id']
        feeds = httpx.get(f'{NYUSEU_HOST}:{NYUSEU_PORT}/api/nyuseu/folders/{folder_id}/feeds/')
        if feeds.status_code == 200:
            folders_and_feeds += feeds.json()
    pprint(folders_and_feeds)
    if folders.status_code == 200:
        return folders.json(), folders_and_feeds
    else:
        return {}, {}


async def home(request):
    """

    """
    folders, folders_and_feeds = await get_feeds_by_folders()
    articles = dict()
    req_articles = httpx.get(f'{NYUSEU_HOST}:{NYUSEU_PORT}/api/nyuseu/articles/')
    if req_articles.status_code == 200:
        articles = req_articles.json()
    template = "index.html"
    context = {"request": request,
               "folders": folders,
               "folders_and_feeds": folders_and_feeds,
               "articles": articles}
    return templates.TemplateResponse(template, context)


async def get_arts_by_feed(request):
    """

    """
    feeds_id = request.path_params['feeds_id']
    folders, folders_and_feeds = await get_feeds_by_folders()
    articles = dict()
    req_articles = httpx.get(f'{NYUSEU_HOST}:{NYUSEU_PORT}/api/nyuseu/feeds/{feeds_id}/articles/')
    if req_articles.status_code == 200:
        articles = req_articles.json()
    template = "index.html"
    context = {"request": request,
               "folders": folders,
               "folders_and_feeds": folders_and_feeds,
               "articles": articles}
    return templates.TemplateResponse(template, context)


NYUSEU_FRONT_BASE_URL = settings('NYUSEU_FRONT_BASE_URL')

# The Routes to static content and main page
frontend = Router(routes=[
    Mount('/', app=Router([
        Route('/', endpoint=home, methods=['GET']),
        Mount('/feeds', app=Router([
            #Route('/', endpoint=get_feeds, methods=['GET']),
            #Route('/{feeds_id}', endpoint=get_feed, methods=['GET']),
            Route('/{feeds_id}/articles', endpoint=get_arts_by_feed, methods=['GET']),
            # Route('/', endpoint=create_feeds, methods=['POST']),
            # Route('/{feeds_id}', endpoint=update_feeds, methods=['PATCH']),
            # Route('/{feeds_id}', endpoint=delete_feeds, methods=['DELETE']),
        ])),
        Mount('/articles', app=Router([
            #Route('/', endpoint=get_arts, methods=['GET']),
            #Route('/{art_id}', endpoint=get_art, methods=['GET']),
            # Route('/', endpoint=create_art, methods=['POST']),
            # Route('/{art_id}', endpoint=update_art, methods=['PATCH']),
            # Route('/{art_id}', endpoint=delete_art, methods=['DELETE']),
        ])),
        Mount('/folders', app=Router([
            #Route('/', endpoint=get_folders, methods=['GET']),
            # Route('/{folder_id}', endpoint=get_folder, methods=['GET']),
            # Route('/{folder_id}/feeds/', endpoint=get_feeds_by_folder, methods=['GET']),
            # Route('/', endpoint=create_folder, methods=['POST']),
            # Route('/{folder_id}', endpoint=update_folder, methods=['PATCH']),
            # Route('/{folder_id}', endpoint=delete_folder, methods=['DELETE']),
        ]))
    ])),
    #Mount(NYUSEU_FRONT_BASE_URL + 'static/css', StaticFiles(directory="static/css")),
    #Mount(NYUSEU_FRONT_BASE_URL + 'static/js', StaticFiles(directory="static/js")),
])

main_app.mount('/', app=frontend)

# Bootstrap
if __name__ == '__main__':
    print('Nyuseu Front - 뉴스 - Feeds Reader - Starlette powered')
    uvicorn.run(main_app,
                host=settings('NYUSEU_FRONT_HOST', default='127.0.0.1'),
                port=settings('NYUSEU_FRONT_PORT',
                              cast=int,
                              default=8003))
