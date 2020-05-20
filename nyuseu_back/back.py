# coding: utf-8
"""
   Nyuseu - 뉴스 - sauce starlette
"""
import logging
import os
# starlette
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Mount, Router, Route
import sys
# uvicorn
import uvicorn

# logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

# API
from nyuseu_api import NyuseuApi

# load configuration
settings = Config('.env')

main_app = Starlette()
main_app.debug = settings('NYUSEU_DEBUG', default=False)

nyuseu = NyuseuApi()


async def get_art(request):
    """
    get one article
    :param request:
    :return:
    """
    art_id = request.path_params['art_id']
    res = await nyuseu.get_art(art_id=art_id)
    logger.debug(res.json())
    return JSONResponse(res.json())


async def get_arts(request):
    """
    get all articles
    :param request:
    :return:
    """
    res = await nyuseu.get_arts()
    logger.debug(res.json())
    return JSONResponse(res.json())


async def get_arts_by_feed(request):
    """
    get all articles of a given feeds
    :param request:
    :return:
    """
    feeds_id = request.path_params['feeds_id']
    res = await nyuseu.get_arts_by_feed(feeds_id)
    logger.debug(res.json())
    return JSONResponse(res.json())


async def create_art(request):
    """
    create an article
    :param request:
    :return:
    """
    payload = await request.json()
    title = payload['title']
    text = payload['text']
    if 'feeds_id' not in payload:
        raise ValueError('Source of Feeds is missing. An article belongs to a Source Feeds')
    feeds_id = payload['feeds_id']
    res = await nyuseu.create_art(title=title, text=text, feeds_id=feeds_id)
    logger.debug(res.json())
    return res


async def update_art(request):
    """
    update a article
    :param request:
    :return:
    """
    art_id = request.path_params['art_id']
    payload = await request.json()
    title = payload['title']
    text = payload['text']
    read = payload['read']
    if 'feeds_id' not in payload:
        raise ValueError('Source Feeds ID is missing. A Feed belongs to a Source Feeds')
    feeds_id = payload['feeds_id']
    res = await nyuseu.update_art(art_id=art_id, title=title, text=text, feeds_id=feeds_id, read=read)
    logger.debug(res.json())
    return res


async def delete_art(request):
    """
    delete an article
    :param request:
    :return:
    """
    feeds_id = request.path_params['feeds_id']
    res = await nyuseu.delete_feeds(feeds_id=feeds_id)
    logger.debug(res.json())
    return res


async def get_feeds(request):
    """
    get one source feeds
    :param request:
    :return:
    """
    res = await nyuseu.get_feeds()
    logger.debug(res.json())
    return JSONResponse(res.json())


async def get_feeds_by_folder(request):
    """
    get all feeds of a given folder
    :param request:
    :return:
    """
    folder_id = request.path_params['folder_id']
    res = await nyuseu.get_feeds_by_folder(folder_id=folder_id)
    logger.debug(res.json())
    return JSONResponse(res.json())


async def get_feed(request):
    """
    get one source feeds
    :param request:
    :return:
    """
    feeds_id = request.path_params['feeds_id']
    res = await nyuseu.get_feed(feeds_id=feeds_id)
    logger.debug(res.json())
    return JSONResponse(res.json())


async def create_feeds(request):
    """
    create a source of feeds
    :param request:
    :return:
    """
    payload = await request.json()
    title = payload['title']
    text = payload['text']
    if 'folder_id' not in payload:
        raise ValueError('Folder is missing. A Source Feeds has to own its own Folder')
    folder_id = payload['folder_id']
    res = await nyuseu.create_feeds(title=title, text=text, folder_id=folder_id)
    logger.debug(res.json())
    return res


async def update_feeds(request):
    """
    update a source of feeds
    :param request:
    :return:
    """
    feeds_id = request.path_params['feeds_id']
    payload = await request.json()
    title = payload['title']
    text = payload['text']
    if 'folder_id' not in payload:
        raise ValueError('Folder is missing. A Source of feeds has to own its own Folder')
    folder_id = payload['folder_id']
    res = await nyuseu.update_feeds(feeds_id=feeds_id, title=title, text=text, folder_id=folder_id)
    logger.debug(res.json())
    return res


async def delete_feeds(request):
    """
    delete a source feeds
    :param request:
    :return:
    """
    feeds_id = request.path_params['feeds_id']
    res = await nyuseu.delete_feeds(feeds_id=feeds_id)
    logger.debug(res.json())
    return res


async def get_folder(request):
    """
    get one folder
    :param request:
    :return:
    """
    folder_id = request.path_params['folder_id']
    res = await nyuseu.get_folder(folder_id=folder_id)
    logger.debug(res.json())
    return JSONResponse(res.json())


async def get_folders(request):
    """
    get all the folders
    :param request:
    :return:
    """
    res = await nyuseu.get_folders()
    logger.debug(res.json())
    return JSONResponse(res.json())


async def create_folder(request):
    """
    create a folder
    :param request:
    :return:
    """
    payload = await request.json()
    title = payload['title']
    res = await nyuseu.create_folder(title=title)
    logger.debug(res.json())
    return res


async def update_folder(request):
    """
    update a folder
    :param request:
    :return:
    """
    folder_id = request.path_params['folder_id']
    payload = await request.json()
    title = payload['title']
    res = await nyuseu.update_folder(folder_id=folder_id, title=title)
    logger.debug(res.json())
    return res


async def delete_folder(request):
    """
    delete a folder
    :param request:
    :return:
    """
    folder_id = request.path_params['folder_id']
    res = await nyuseu.delete_folder(folder_id=folder_id)
    logger.debug(res.json())
    return res

# The API Routes
api = Router(routes=[
    Mount('/nyuseu', app=Router([
        Mount('/feeds', app=Router([
            Route('/', endpoint=get_feeds, methods=['GET']),
            Route('/{feeds_id}', endpoint=get_feed, methods=['GET']),
            Route('/{feeds_id}/articles', endpoint=get_arts_by_feed, methods=['GET']),
            Route('/', endpoint=create_feeds, methods=['POST']),
            Route('/{feeds_id}', endpoint=update_feeds, methods=['PATCH']),
            Route('/{feeds_id}', endpoint=delete_feeds, methods=['DELETE']),
        ])),
        Mount('/articles', app=Router([
            Route('/', endpoint=get_arts, methods=['GET']),
            Route('/{art_id}', endpoint=get_art, methods=['GET']),
            Route('/', endpoint=create_art, methods=['POST']),
            Route('/{art_id}', endpoint=update_art, methods=['PATCH']),
            Route('/{art_id}', endpoint=delete_art, methods=['DELETE']),
        ])),
        Mount('/folders', app=Router([
            Route('/', endpoint=get_folders, methods=['GET']),
            Route('/{folder_id}', endpoint=get_folder, methods=['GET']),
            Route('/{folder_id}/feeds/', endpoint=get_feeds_by_folder, methods=['GET']),
            Route('/', endpoint=create_folder, methods=['POST']),
            Route('/{folder_id}', endpoint=update_folder, methods=['PATCH']),
            Route('/{folder_id}', endpoint=delete_folder, methods=['DELETE']),
        ]))
    ]))
])


# The Routes to static content and main page
frontend = Router(routes=[
    # Mount('/files', StaticFiles(directory=settings('NYUSEU_FILE'))),
    # Mount(NYUSEU_BASE_URL + 'static/css', StaticFiles(directory="static/css")),
    # Mount(NYUSEU_BASE_URL + 'static/js', StaticFiles(directory="static/js")),
])

# let's mount each Route
main_app.mount('/api', app=api)
main_app.mount('/', app=frontend)

# Bootstrap
if __name__ == '__main__':
    print('Nyuseu Back - 뉴스 - Feeds Reader - Starlette powered')
    uvicorn.run(main_app,
                host=settings('NYUSEU_HOST', default='127.0.0.1'),
                port=settings('NYUSEU_PORT',
                              cast=int,
                              default=8002))
