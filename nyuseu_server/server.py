# coding: utf-8
"""
   Nyuseu - 뉴스 - Server
"""
import json
import logging
import orm
import os
# starlette
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Mount, Router, Route
from starlette.schemas import SchemaGenerator
import sys
# uvicorn
import uvicorn
import yaml

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

import nyuseu_server  # noqa: E402
from nyuseu_server.models import Feeds, Folders, Articles  # noqa: E402
from nyuseu_server.models import database  # noqa: E402
from nyuseu_server.opml_load import load  # noqa: E402

logger = logging.getLogger(__name__)

# load configuration
settings = Config('.env')

schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Nyuseu Server API", "version": "1.0"}}
)

main_app = Starlette()
main_app.debug = settings('NYUSEU_SERVER_DEBUG', default=False)


# FOLDERS
async def get_folder(request):
    """
    responses:
      200:
        description: get a folder.
        examples:
          [{"id": 1,
           "title": "My folder name",
           "date_created": "2020-05-12T01:00",
           "date_modified": "2020-05-12T18:27:08"}
           ]
    """
    folder_id = request.path_params['folder_id']
    folder = await Folders.objects.get(id=folder_id)
    payload = {'id': folder.id,
               'title': folder.title,
               'date_created': str(folder.date_created),
               'date_modified': str(folder.date_modified),
               }
    logger.debug(f"get a folder {folder.title}")
    return JSONResponse(payload)


async def get_feeds_by_folder(request):
    """
    responses:
      200:
        description: get the list of folders and the feeds
        examples:
          [{"id": 1,
            "title": "My folder name",
            "date_created": "2020-05-10T01:00",
            "date_modified": "2020-05-10T12:00",
            "unread": 0,
            "feeds": [{
               "id": 1,
               "title": "Books",
               "url": "https://wikipedia.org",
               "date_created": "2020-04-01T00:00:00",
               "date_modified": "2020-04-01T01:00:00",
               "date_grabbed": "2020-06-01T00:00:00",
               "status": 1},
               {"id": 2,
               "title": "Cooking",
               "url": "https://www.maangchi.com/",
               "date_created": "2020-04-01T00:00:00",
               "date_modified": "2020-04-01T01:00:00",
               "date_grabbed": "2020-06-01T00:00:00",
               "status": 1}
               ]
          }]
    """
    folder_id = request.path_params['folder_id']

    data = await Feeds.objects.filter(folder__id=folder_id).all()
    content = [
        {
            "id": result["id"],
            "title": result["title"],
            "url": result["url"],
            "folder": {'id': result.folder.id,
                       'title': result.folder.title,
                       'date_created': str(result.folder.date_created),
                       'date_modified': str(result.folder.date_modified)
                       },
            "date_created": str(result["date_created"]),
            "date_modified": str(result["date_modified"]),
            "status": result["status"],
        }
        for result in data
    ]

    logger.debug(f"get feeds of the folder {folder_id}")
    return JSONResponse(content)


async def get_folders(request):
    """
    responses:
      200:
        description: get the list of folders and the feeds
        examples:
          [{"id": 1,
            "title": "My folder name",
            "date_created": "2020-05-10T01:00",
            "date_modified": "2020-05-10T12:00",
            "unread": 0,
            "feeds": {
               "id": 1,
               "title": "Books",
               "url": "https://wikipedia.org",
               "date_created": "2020-04-01T00:00:00",
               "date_modified": "2020-04-01T01:00:00",
               "date_grabbed": "2020-06-01T00:00:00",
               "status": 1}
          },
          {"id": 2,
           "title": "My folder name2",
           "date_created": "2020-05-10T01:00",
           "date_modified": "2020-05-10T01:00",
           "unread": 12,
           "feeds": {
              "id": 1,
              "title": "Books",
              "url": "https://wikipedia.org",
              "date_created": "2020-04-01T00:00:00",
              "date_modified": "2020-04-01T01:00:00",
              "date_grabbed": "2020-06-01T00:00:00",
              "status": 1}
          }]
    """
    # raw SQL to retrieve in same time, the folders + number of unread articles
    query = """
    SELECT folders.id,
       folders.title,
       folders.date_created,
       folders.date_modified,
       COUNT(CASE WHEN NOT articles.read THEN '1' ELSE NULL END) AS unread
  FROM folders
  LEFT OUTER JOIN feeds
    ON (folders.id = feeds.folder)
  LEFT OUTER JOIN articles
    ON (feeds.id = articles.feeds)
 GROUP BY folders.id,
       folders.title,
       folders.date_created,
       folders.date_modified
    """
    data = await database.fetch_all(query=query)
    content = []
    for result in data:
        data_feed = await Feeds.objects.filter(folder__id=result['id']).all()
        content_feed = [
            {
                "id": result_feed["id"],
                "title": result_feed["title"],
                "url": result_feed["url"],
                "date_created": str(result_feed["date_created"]),
                "date_modified": str(result_feed["date_modified"]),
                "status": result_feed["status"],
            }
            for result_feed in data_feed
        ]

        content.append({
            "id": result["id"],
            "title": result["title"],
            "date_created": result["date_created"],
            "date_modified": result["date_modified"],
            "unread": result["unread"],
            "feeds": content_feed
        })

    logger.debug("get list of folders")
    return JSONResponse(content)


async def create_folder(request):
    """
    responses:
      200:
        description: create a folder.
        examples:
          [{"title": "FolderA"}]
    """
    payload = await request.json()
    title = payload['title']
    try:
        res = await Folders.objects.get(title=title)
    except orm.exceptions.NoMatch:
        res = await Folders.objects.create(title=title)
    data = json.dumps({'title': title, 'id': res.id})
    logger.debug(data)
    return JSONResponse(data)


async def update_folder(request):
    """
    responses:
      200:
        description: update a folder.
        examples:
          [{"id": 1}, {"title": "FolderB"}]
    """
    folder_id = request.path_params['folder_id']
    payload = await request.json()
    title = payload['title']
    try:
        folder = await Folders.objects.get(id=folder_id)
        res = await folder.update(title=title)
    except orm.exceptions.NoMatch as e:
        raise ValueError(f"Folder {folder_id} not found - {e}")
    logger.debug(f"update a folder {folder_id}")
    return JSONResponse(res.json())


async def delete_folder(request):
    """
    responses:
      200:
        description: delete a folder.
        examples:
          [{"id": 1}]
    """
    folder_id = request.path_params['folder_id']
    try:
        folder = await Folders.objects.get(id=folder_id)
        res = await folder.delete(id=folder_id)
    except orm.exceptions.NoMatch as e:
        raise ValueError(f"Folder {folder_id} not found - {e}")
    logger.debug(f"delete a folder {folder_id}")
    return JSONResponse(res.json())


# SOURCE FEEDS
async def get_feed(request):
    """
    responses:
      200:
        description: get a source of feeds.
        examples:
          [{"id": 1,
          "title": "Github Rss Feeds",
          "url": "https://github.com/rss",
          "folder": {
              "id": 1,
              "title": "Project",
              "date_created": "2020-04-01T00:00:00",
              "date_modified": "2020-04-01T01:00:00"
            },
          "date_created": "2020-05-12T01:00",
          "date_modified": "2020-05-12T18:27",
          "status": 1}
          ]
    """
    feeds_id = request.path_params['feeds_id']
    feeds = await Feeds.objects.select_related("folder").get(id=feeds_id)

    payload = {'id': feeds.id,
               'title': feeds.title,
               'url': feeds.url,
               "folder": {'id': feeds.folder.id,
                          'title': feeds.folder.title,
                          'date_created': str(feeds.folder.date_created),
                          'date_modified': str(feeds.folder.date_modified)
                          },
               'date_created': str(feeds.date_created),
               'date_modified': str(feeds.date_modified),
               'status': feeds.status}
    logger.debug(f"get a source feeds {payload}")
    return JSONResponse(payload)


async def get_feeds(request):
    """
    responses:
      200:
        description: get the list of source of feeds
        examples:
          [{"id": 1,
          "title": "Github Rss Feeds",
          "url": "https://github.com/rss",
          "folder": {"id": 1,
            "title": "Project",
            "date_created": "2020-04-01T00:00:00",
            "date_modified": "2020-04-01T01:00:00"
            },
          "date_created": "2020-05-12T01:00",
          "date_modified": "2020-05-12T18:27:2",
          "status": 1}
          ]
    """
    data = await Feeds.objects.select_related("folder").all()
    content = [
        {
            "id": result["id"],
            "title": result["title"],
            "url": result["url"],
            "folder": {'id': result.folder.id,
                       'title': result.folder.title,
                       'date_created': str(result.folder.date_created),
                       'date_modified': str(result.folder.date_modified)
                       },
            "date_created": str(result["date_created"]),
            "date_modified": str(result["date_modified"]),
            "status": result["status"],
        }
        for result in data
    ]
    logger.debug("get all Source of Feeds")
    return JSONResponse(content)


async def create_feeds(request):
    """
    responses:
      200:
        description: create a source of feeds.
        examples:
          [{"title": "Github Rss Feeds", "url": "https://github.com/rss", "folder": 1}]
    """
    payload = await request.json()
    title = payload['title']
    url = payload['url']
    if 'folder_id' not in payload:
        raise ValueError('Folder is missing. A Source of feeds has to own its own Folder')
    folder_id = payload['folder_id']
    try:
        folder = await Folders.objects.get(id=folder_id)
        try:
            res = await Feeds.objects.get(title=title)

        except orm.exceptions.NoMatch:
            res = await Feeds.objects.create(title=title, url=url, folder=folder, status=True)
        if res:
            logger.debug(f"create a source feeds {res.id}:{res.title} {res.url}")
            return JSONResponse(json.dumps({'id': res.id,
                                            'title': res.title,
                                            'folder': res.folder.id,
                                            'url': res.url,
                                            'date_created': str(res.date_created),
                                            'date_modified': str(res.date_modified),
                                            'date_triggered': str(res.date_triggered),
                                            'status': res.status}))
        else:
            raise ValueError(res)
    except orm.exceptions.NoMatch as e:
        raise ValueError(f"Folder {folder_id} not found, no source feeds created - {e}")


async def update_feeds(request):
    """
    responses:
      200:
        description: update a source of feeds.
        examples:
          [{"id": 1, "title": "Github Rss Feeds", "url": "https://github.com/rss", "folder": 1, "status": True}]
    """
    feeds_id = request.path_params['feeds_id']
    payload = await request.json()
    title = payload['title']
    folder_id = payload['folder_id']
    status = payload['status']
    url = payload['url']
    try:
        folder = await Folders.objects.get(id=folder_id)
    except orm.exceptions.NoMatch as e:
        raise ValueError(f"Folder {folder_id} not found - {e}")

    feeds_id = await Feeds.objects.get(id=feeds_id)
    if folder:
        res = await Feeds.update(title=title,
                                 folder=folder,
                                 url=url,
                                 status=True if status else False)
    else:  # folder has not been found, update the source_feeds without the folder
        res = await Feeds.update(title=title,
                                 url=url,
                                 status=True if status else False)
    logger.debug(f"update a source feeds {feeds_id}:{title}")
    return JSONResponse(res.json())


async def delete_feeds(request):
    """
    responses:
      200:
        description: delete a source of feeds.
        examples:
          [{"id": 1}]
    """
    feeds_id = request.path_params['feeds_id']
    try:
        source_feeds = await Feeds.objects.get(id=feeds_id)
        res = await source_feeds.delete(id=feeds_id)
    except orm.exceptions.NoMatch as e:
        raise ValueError(f"Source Feeds {feeds_id} not found - {e}")
    logger.debug(f"delete a Source Feeds {feeds_id}")
    return JSONResponse(res.json())


# ARTICLES
async def get_art(request):
    """
    responses:
      200:
        description: get an article.
        examples:
          [{"id": 1,
           "title": "A great article",
           "text": "Once upon a time",
           "image": "",
           "source_url": "https://github.com/rss",
           "read": 0,
           "read_later": 1,
           "date_created": "2020-04-01T00:00:00",
           "feeds": {
               "id": 1,
               "title": "Books",
               "url": "https://wikipedia.org",
               "folder":
                 {"id": 1, "title": "Project", "date_created": "2020-04-01T00:00:00",
                                               "date_modified": "2020-04-01T01:00:00"},
               "date_created": "2020-04-01T00:00:00",
               "date_modified": "2020-04-01T01:00:00",
               "date_grabbed": "2020-06-01T00:00:00",
               "status": 1}
           }]
    """
    art_id = request.path_params['art_id']
    result = await Articles.objects.select_related("feeds").get(id=art_id)

    folder = await Folders.objects.get(id=result.feeds.folder.id)

    my_folder = {'id': folder.id,
                 'title': folder.title,
                 'date_created': str(folder.date_created),
                 'date_modified': str(folder.date_modified)
                 }
    content = {
        "id": result["id"],
        "title": result["title"],
        "text": result["text"],
        "image": result["image"],
        "feeds": {'id': result.feeds.id,
                  'title': result.feeds.title,
                  'url': result.feeds.url,
                  'folder': my_folder,
                  'date_created': str(result.feeds.date_created),
                  'date_modified': str(result.feeds.date_modified),
                  'date_grabbed': str(result.feeds.date_grabbed),
                  'status': result.feeds.status,
                  },
        "date_created": str(result["date_created"]),
        "source_url": result["source_url"],
        "read": result["read"],
        "read_later": result["read_later"],
    }

    logger.debug(f"get an article {result}")
    return JSONResponse(content)


async def get_arts(request):
    """
    responses:
      200:
        description: get all articles.
        examples:
          [{"id": 1,
           "title": "A great article",
           "text": "Once upon a time",
           "image": "",
           "source_url": "https://github.com/rss",
           "read": 0,
           "read_later": 1,
           "date_created": "2020-04-01T00:00:00",
           "feeds": {
               "id": 1,
               "title": "Books",
               "url": "https://wikipedia.org",
               "folder":
                 {"id": 1, "title": "Project", "date_created": "2020-04-01T00:00:00",
                                               "date_modified": "2020-04-01T01:00:00"},
               "date_created": "2020-04-01T00:00:00",
               "date_modified": "2020-04-01T01:00:00",
               "date_grabbed": "2020-06-01T00:00:00",
               "status": 1}
           }]
    """
    content = []
    data = await Articles.objects.select_related("feeds").all()

    for result in data:
        folder = await Folders.objects.get(id=result.feeds.folder.id)

        my_folder = {'id': folder.id,
                     'title': folder.title,
                     'date_created': str(folder.date_created),
                     'date_modified': str(folder.date_modified)
                     }
        content.append(
            {
                "id": result["id"],
                "title": result["title"],
                "text": result["text"],
                "image": result["image"],
                "feeds": {'id': result.feeds.id,
                          'title': result.feeds.title,
                          'url': result.feeds.url,
                          "folder": my_folder,
                          'date_created': str(result.feeds.date_created),
                          'date_modified': str(result.feeds.date_modified),
                          'date_grabbed': str(result.feeds.date_grabbed),
                          'status': result.feeds.status,
                          },
                "date_created": str(result["date_created"]),
                "source_url": result["source_url"],
                "read": result["read"],
                "read_later": result["read_later"],
            }
        )
    logger.debug("get all articles")
    return JSONResponse(content)


async def get_arts_by_feed(request):
    """
    responses:
      200:
        description: get articles by feeds id
        examples:
          [{"id": 1,
           "title": "A great article",
           "text": "Once upon a time",
           "image": "",
           "source_url": "https://github.com/rss",
           "read": 0,
           "read_later": 1,
           "date_created": "2020-04-01T00:00:00",
           "feeds": {
               "id": 1,
               "title": "Books",
               "url": "https://wikipedia.org",
               "folder":
                 {"id": 1, "title": "Project", "date_created": "2020-04-01T00:00:00",
                                               "date_modified": "2020-04-01T01:00:00"},
               "date_created": "2020-04-01T00:00:00",
               "date_modified": "2020-04-01T01:00:00",
               "date_grabbed": "2020-06-01T00:00:00",
               "status": 1}
           }]
    """
    feeds_id = request.path_params['feeds_id']
    content = []
    data = await Articles.objects.filter(feeds__id=feeds_id).all()

    for result in data:
        folder = await Folders.objects.get(id=result.feeds.folder.id)

        my_folder = {'id': folder.id,
                     'title': folder.title,
                     'date_created': str(folder.date_created),
                     'date_modified': str(folder.date_modified)
                     }
        content.append(
            {
                "id": result["id"],
                "title": result["title"],
                "text": result["text"],
                "image": result["image"],
                "feeds": {'id': result.feeds.id,
                          'title': result.feeds.title,
                          'url': result.feeds.url,
                          "folder": my_folder,
                          'date_created': str(result.feeds.date_created),
                          'date_modified': str(result.feeds.date_modified),
                          'date_grabbed': str(result.feeds.date_grabbed),
                          'status': result.feeds.status,
                          },
                "date_created": str(result["date_created"]),
                "source_url": result["source_url"],
                "read": result["read"],
                "read_later": result["read_later"],
            }
        )
    logger.debug(f"get all articles for that feed {feeds_id}")
    return JSONResponse(content)


async def mark_as_read(request):
    """
    responses:
      200:
        description: mark an article as read
        examples:
          [{"id": 1, "read": 1}]
    """
    art_id = request.path_params['art_id']
    art = await Articles.objects.get(id=art_id)
    res = await art.update(read=True)
    logger.debug(f"update article {art_id} {art.title}")
    return JSONResponse(res.json())


async def mark_as_unread(request):
    """
    responses:
      200:
        description: mark an article as read
        examples:
          [{"id": 1, "read": 0}]
    """
    art_id = request.path_params['art_id']
    art = await Articles.objects.get(id=art_id)
    res = await art.update(read=False)
    logger.debug(f"update article {art_id} {art.title}")
    return JSONResponse(res.json())


async def read_later(request):
    """
    responses:
      200:
        description: mark an article as "read later"
        examples:
          [{"id": 1, "read_later": 1}]
    """
    art_id = request.path_params['art_id']
    art = await Articles.objects.get(id=art_id)
    res = await art.update(read_later=True)
    logger.debug(f"update article {art_id} {art.title}")
    return JSONResponse(res.json())


async def unread_later(request):
    """
    responses:
      200:
        description: mark an article as not "read later"
        examples:
          [{"id": 1, "read_later": 0}]
    """
    art_id = request.path_params['art_id']
    art = await Articles.objects.get(id=art_id)
    res = await art.update(read_later=False)
    logger.debug(f"update article {art_id} {art.title}")
    return JSONResponse(res.json())


async def opml(request):
    """
    responses:
      200:
        description: import an OPML file
        examples:
          [{"opml": "http://url/to/opml or /local/path/to/opml/file"}]
    """
    opml_resource = request.path_params['opml']
    if opml_resource.endswith('.opml'):
        res = await load(opml_resource)
    else:
        res = json.dumps({'status': 'the file is not an OPML file'})
    logger.debug(res.json())
    return JSONResponse(res.json())


async def server_check(request):
    """
    responses:
      200:
        description: get the version of the server
        examples:
          [{"version": "0.0.1"}]
    """
    version = {'version': nyuseu_server.__version__}
    logger.debug(version)
    return JSONResponse(version)


def openapi_schema(request):
    """

    """
    return schemas.OpenAPIResponse(request=request)


# The API Routes
app = Router(routes=[
    Mount('/nyuseu', app=Router([
        Mount('/folders', app=Router([
            Route('/', endpoint=get_folders, methods=['GET']),
            Route('/{folder_id}/feeds/', endpoint=get_feeds_by_folder, methods=['GET']),
            Route('/{folder_id}', endpoint=get_folder, methods=['GET']),
            Route('/', endpoint=create_folder, methods=['POST']),
            Route('/{folder_id}', endpoint=update_folder, methods=['PATCH']),
            Route('/{folder_id}', endpoint=delete_folder, methods=['DELETE']),
        ])),
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
            Route('/{art_id}/marked_as_read', endpoint=mark_as_read, methods=['PATCH']),
            Route('/{art_id}/marked_as_unread', endpoint=mark_as_unread, methods=['PATCH']),
            Route('/{art_id}/read_later', endpoint=read_later, methods=['PATCH']),
            Route('/{art_id}/unread_later', endpoint=unread_later, methods=['PATCH'])
        ])),
        Mount('/version', app=Router([
            Route('/', endpoint=server_check, methods=['GET']),
        ])),
        Mount('/import', app=Router([
            Route('/opml', endpoint=opml, methods=['POST']),
        ])),
        Route("/schema", endpoint=openapi_schema, include_in_schema=False)
    ]))
])

# let's mount each Route
main_app.mount('/api', app=app)

# Bootstrap
if __name__ == '__main__':
    print('Nyuseu Server - 뉴스 - Feeds Reader Server - Starlette powered')

    if sys.argv[-1] == "schema":
        schema = schemas.get_schema(routes=app.routes)
        print(yaml.dump(schema, default_flow_style=False))
    else:
        uvicorn.run(main_app,
                    host=settings('NYUSEU_SERVER_HOST', default='127.0.0.1'),
                    port=settings('NYUSEU_SERVER_PORT',
                                  cast=int,
                                  default=8001))
