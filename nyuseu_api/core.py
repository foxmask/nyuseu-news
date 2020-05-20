# coding: utf-8
"""
   Nyuseu - 뉴스 - sauce starlette
"""
import json
import logging
import httpx
from httpx import Response
from starlette.config import Config

logger = logging.getLogger(__name__)

__author__ = 'FoxMaSk'
__all__ = ['NyuseuApi']

# load configuration
settings = Config('.env')


SERVER = settings('NYUSEU_URL_SERVER', default='http://127.0.0.1:8001')


class NyuseuApi:

    SERVER = ''

    def __init__(self):
        self.SERVER = settings.get('NYUSEU_URL_SERVER', default='http://127.0.0.1:8001')
        self.client = httpx.AsyncClient()

    async def query(self, method: str, path: str, **payload: dict) -> Response:
        full_path = self.SERVER + '/nyuseu' + path
        if method == 'get':
            if 'folder' in payload:
                # get 'sources feeds' for a given folder
                res = await self.client.get(full_path, params={'folder': payload['folder']})
            elif 'feeds' in payload:
                # get 'article' for a given 'source feeds'
                res = await self.client.get(full_path, params={'feeds': payload['feeds']})
            else:
                res = await self.client.get(full_path)
        elif method == 'post':
            res = await self.client.post(full_path, json=payload)
        elif method == 'put':
            headers = {'Content-Type': 'application/json'}
            res = await self.client.post(full_path, data=json.dumps(payload), headers=headers)
        elif method == 'delete':
            res = await self.client.delete(full_path)
        res.raise_for_status()
        return res

    async def create_art(self, title: str, text: str, feeds_id: int) -> Response:
        """
        POST /articles

        create an article
        :param title: string
        :param text: string
        :param feeds_id: id of source feeds
        :return: res: json result of the post
        """
        data = {
            'title': title,
            'text': text,
            'feeds_id': feeds_id,
            'read': False
        }

        return await self.query('post', '/articles', **data)

    async def update_art(self, art_id: int, title: str, text: str, feeds_id: int, read: bool) -> Response:
        """
        PUT /articles/:art_id

        update an article
        :param art_id: id of the article
        :param title: string
        :param text: string
        :param feeds_id: id of the feeds
        :param read: boolean of the article
        :return: res: json result of the post
        """
        data = {
            'title': title,
            'text': text,
            'feeds_id': feeds_id,
            'read': read
        }
        return await self.query('put', f'/articles/{art_id}', **data)

    async def delete_art(self, art_id: int) -> Response:
        """
        DELETE /articles/:art_id

        delete an article
        :param art_id: id of the article
        :return: res: json result of the post
        """
        return await self.query('delete', f'/artcles/{art_id}')

    async def get_art(self, art_id: int) -> Response:
        """
        GET /articles/:art_id
        get one article
        :param art_id: id of the article
        :return: res: result of the get
        """
        return await self.query('get', f'/articles/{art_id}')

    async def get_arts(self, **kwargs: dict) -> Response:
        """
        GET /articles
        get all articles
        :return: res: result of the get
        """
        return await self.query('get', '/articles/', **kwargs)

    async def get_arts_by_feed(self, feeds_id: int) -> Response:
        """
        GET /feeds/:feeds_id/articles/
        get all articles of a given feeds
        :param feeds_id: int of the feeds
        :return: res: result of the get
        """
        return await self.query('get', f'/feeds/{feeds_id}/articles/')

    async def create_feeds(self, title: str, text: str, folder_id: int) -> Response:
        """
        POST /feeds

        create a source feed
        :param title: string
        :param text: string
        :param folder_id: string id of the parent folder
        :return: res: json result of the post
        """
        data = {
            'title': title,
            'text': text,
            'folder_id': folder_id,
            'read': False
        }

        return await self.query('post', '/feeds', **data)

    async def update_feeds(self, feeds_id: int, title: str, text: str, folder_id: int, ) -> Response:
        """
        PUT /feeds/:feeds_id

        update a feeds
        :param feeds_id: integer
        :param title: string
        :param text: string
        :param folder_id: string id of the parent folder
        :return: res: json result of the post
        """
        data = {
            'title': title,
            'text': text,
            'folder_id': folder_id,
        }
        return await self.query('put', f'/feeds/{feeds_id}', **data)

    async def delete_feeds(self, feeds_id: int) -> Response:
        """
        DELETE /feeds/:feeds_id

        delete a feeds
        :param feeds_id: integer
        :return: res: json result of the post
        """
        return await self.query('delete', f'/feeds/{feeds_id}')

    async def get_feed(self, feeds_id: int) -> Response:
        """
        GET /feeds/:feeds_id
        get one source of feeds
        :param feeds_id: id of the source of feeds
        :return: res: result of the get
        """
        return await self.query('get', f'/feeds/{feeds_id}')

    async def get_feeds(self, **kwargs: dict) -> Response:
        """
        GET /feeds

        get all sources feeds
        :return: res: result of the get
        """
        return await self.query('get', '/feeds/', **kwargs)

    async def create_folder(self, title: str) -> Response:
        """
        POST /folder

        create a folder
        :param title: string
        :return: res: json result of the post
        """
        return await self.query('post', '/folders', **{'title': title})

    async def update_folder(self, folder_id: int, title: str) -> Response:
        """
        PUT /folder/:folder_id

        update a folder
        :param folder_id: integer
        :param title: string of the folder
        :return: res: json result of the post
        """
        return await self.query('put', f'/folder/{folder_id}', **{'title': title})

    async def delete_folder(self, folder_id: int) -> Response:
        """
        DELETE /folder/:folder_id

        delete a folder
        :param folder_id: integer
        :return: res: json result of the post
        """
        return await self.query('delete', f'/folder/{folder_id}')

    async def get_feeds_by_folder(self, folder_id: int):
        """
        GET /folders/:folder_id/feeds/
        get feeds of a given folder
        :param folder_id: id of the folder
        :return: res: result of the get
        """
        return await self.query('get', f'/folders/{folder_id}/feeds/')

    async def get_folder(self, folder_id: int) -> Response:
        """
        GET /folders/:folder_id
        get one folder
        :param folder_id: id of the folder
        :return: res: result of the get
        """
        return await self.query('get', f'/folders/{folder_id}')

    async def get_folders(self) -> Response:
        """
        GET /folders
        get all the folders
        :return: res: result of the get
        """
        return await self.query('get', '/folders/')
