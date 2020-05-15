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

    async def create_art(self, title: str, text: str, source_feeds_id: str) -> Response:
        """
        POST /articles

        create an article
        :param title: string
        :param text: string
        :param source_feeds_id: id of source feeds
        :return: res: json result of the post
        """
        data = {
            'title': title,
            'text': text,
            'source_feeds_id': source_feeds_id,
            'read': False
        }

        return await self.query('post', '/articles', **data)

    async def update_art(self, art_id: str, title: str, text: str, source_feeds_id: str, read: bool) -> Response:
        """
        PUT /articles/:art_id

        update an article
        :param art_id: id of the article
        :param title: string
        :param text: string
        :param source_feeds_id: id of the source_feeds
        :param read: boolean of the article
        :return: res: json result of the post
        """
        data = {
            'title': title,
            'text': text,
            'source_feeds_id': source_feeds_id,
            'read': read
        }
        return await self.query('put', f'/articles/{art_id}', **data)

    async def delete_art(self, art_id: str) -> Response:
        """
        DELETE /articles/:art_id

        delete an article
        :param art_id: id of the article
        :return: res: json result of the post
        """
        return await self.query('delete', f'/artcles/{art_id}')

    async def get_art(self, art_id: str) -> Response:
        """
        GET /articles/:art_id
        get one article
        :param art_id: id of the article
        :return: res: result of the get
        """
        return await self.query('get', f'/articles/{art_id}')

    async def get_all_arts(self) -> Response:
        """
        GET /articles
        get all articles
        :return: res: result of the get
        """
        return await self.query('get', '/articles/')

    async def create_source_feeds(self, title: str, text: str, folder_id: str) -> Response:
        """
        POST /source_feeds

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

        return await self.query('post', '/source_feeds', **data)

    async def update_source_feeds(self, source_feeds_id: str, title: str, text: str, folder_id: str, ) -> Response:
        """
        PUT /source_feeds/:source_feeds_id

        update a source_feeds
        :param source_feeds_id: integer
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
        return await self.query('put', f'/source_feeds/{source_feeds_id}', **data)

    async def delete_source_feeds(self, source_feeds_id: str) -> Response:
        """
        DELETE /source_feeds/:source_feeds_id

        delete a source_feeds
        :param source_feeds_id: integer
        :return: res: json result of the post
        """
        return await self.query('delete', f'/source_feeds/{source_feeds_id}')

    async def get_source_feeds(self, source_feeds_id: str) -> Response:
        """
        GET /source_feeds/:source_feeds_id
        get one source of feeds
        :param source_feeds_id: id of the source of feeds
        :return: res: result of the get
        """
        return await self.query('get', f'/source_feeds/{source_feeds_id}')

    async def get_all_source_feeds(self) -> Response:
        """
        GET /source_feeds

        get all sources feeds
        :return: res: result of the get
        """
        return await self.query('get', '/source_feeds/')

    async def create_folder(self, title: str) -> Response:
        """
        POST /folder

        create a folder
        :param title: string
        :return: res: json result of the post
        """
        return await self.query('post', '/folders', **{'title': title})

    async def update_folder(self, folder_id: str, title: str) -> Response:
        """
        PUT /folder/:folder_id

        update a folder
        :param folder_id: integer
        :param title: string of the folder
        :return: res: json result of the post
        """
        return await self.query('put', f'/folder/{folder_id}', **{'title': title})

    async def delete_folder(self, folder_id: str) -> Response:
        """
        DELETE /folder/:folder_id

        delete a folder
        :param folder_id: integer
        :return: res: json result of the post
        """
        return await self.query('delete', f'/folder/{folder_id}')

    async def get_folders(self, folder_id: str) -> Response:
        """
        GET /folders/:folder_id
        get one folder
        :param folder_id: id of the folder
        :return: res: result of the get
        """
        return await self.query('get', f'/folders/{folder_id}')

    async def get_all_folders(self) -> Response:
        """
        GET /folders
        get all the folders
        :return: res: result of the get
        """
        return await self.query('get', '/folders/')
