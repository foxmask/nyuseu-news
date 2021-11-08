import os
import sys
import pytz

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))  # noqa: E402
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

from nyuseu_server import settings  # noqa: E402


def test_envfile():

    assert settings.NYUSEU_SERVER_DEBUG is True
    assert settings.NYUSEU_DATABASE_URL == "sqlite:///db.sqlite3"
    assert settings.NYUSEU_SERVER_HOST == '127.0.0.1'
    assert settings.NYUSEU_SERVER_PORT == 8001
    assert settings.TIME_ZONE == 'Asia/Seoul'
    assert settings.BYPASS_BOZO is True
    assert settings.TIME_ZONE in pytz.all_timezones
