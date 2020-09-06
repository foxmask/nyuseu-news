import os
from starlette.config import Config
from starlette.datastructures import URL


def test_envfile(tmpdir):
    path = os.path.join(tmpdir, ".env")
    with open(path, "w") as file:
        file.write("NYUSEU_DATABASE_URL=sqlite:///db.sqlite3\n")
        file.write("NYUSEU_SERVER_DEBUG=True\n")
        file.write("NYUSEU_SERVER_PORT=8001\n")
        file.write("BYPASS_BOZO=True\n")
        file.write("TIME_ZONE=Europe/Paris\n")
        file.write("\n")

    settings = Config(path, environ={"DEBUG": "true"})
    NYUSEU_SERVER_DEBUG = settings("NYUSEU_SERVER_DEBUG", cast=bool)
    NYUSEU_SERVER_PORT = settings("NYUSEU_SERVER_PORT", cast=int, default=8001)
    NYUSEU_DATABASE_URL = settings("NYUSEU_DATABASE_URL", cast=URL)
    BYPASS_BOZO = settings("BYPASS_BOZO", cast=bool)
    TIME_ZONE = settings("TIME_ZONE")

    assert NYUSEU_SERVER_DEBUG is True
    assert NYUSEU_DATABASE_URL.path == "/db.sqlite3"
    assert NYUSEU_DATABASE_URL.password is None
    assert NYUSEU_DATABASE_URL.username is None
    assert BYPASS_BOZO is True
    assert NYUSEU_SERVER_PORT == 8001
    assert TIME_ZONE == 'Europe/Paris'
