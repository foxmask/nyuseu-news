from starlette.config import Config

config = Config(".env")

TIME_ZONE = config('TIME_ZONE', default='Asia/Seoul')
BYPASS_BOZO = config('BYPASS_BOZO', cast=bool, default=True)

NYUSEU_SERVER_DEBUG = config('NYUSEU_SERVER_DEBUG', cast=bool, default=False)
NYUSEU_SERVER_HOST = config('NYUSEU_SERVER_HOST', default='http://127.0.0.1')
NYUSEU_SERVER_PORT = config('NYUSEU_SERVER_PORT', cast=int, default=8001)
NYUSEU_DATABASE_URL = config('NYUSEU_DATABASE_URL', default='sqlite:///db.sqlite3')
