# coding: utf-8
"""
   nyuseu sauce starlette
"""
import httpx
import json
# starlette
from starlette.applications import Starlette
from starlette.config import Config

from starlette.websockets import WebSocket
import os
import sys
# nyuseu_server
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

# load configuration
settings = Config('.env')


main_app = Starlette()
main_app.debug = settings('NYUSEU_SERVER_DEBUG', default=False)


async def create():
    url = 'http://127.0.0.1:8001/nyuseu/folders/'
    payload = json.dumps({'title': 'test'})
    res = httpx.post(url, data=payload)
    print(res.status_code)
    if res.status_code == 200:
        url = 'http://127.0.0.1:8001/nyuseu/folders/1'
        res2 = httpx.get(url)
        if res2.status_code == 200:
            data2 = res2.json()
            print(data2)
            url = 'http://127.0.0.1:8001/nyuseu/source_feeds/'
            payload = json.dumps({'title': 'test',
                                  'url': 'https://foxmask.net/feeds/all.rss.xml',
                                  'folder_id': data2['id']})
            print(payload)
            res3 = httpx.post(url, data=payload)
            print(res3.status_code)
            if res3.status_code == 200:
                url = 'http://127.0.0.1:8001/nyuseu/source_feeds/1'
                res4 = httpx.get(url)
                if res4.status_code == 200:
                    data4 = res4.json()
                    print("create article ", data4)
                    url = 'http://127.0.0.1:8001/nyuseu/articles/'
                    payload = json.dumps({'title': 'test', 'text': 'super test', 'source_feeds_id': data4['id']})
                    print("payload pour article", payload)
                    res5 = httpx.post(url, data=payload)
                    print(res5.status_code)


# Bootstrap
if __name__ == '__main__':
    import asyncio
    asyncio.run(create())

