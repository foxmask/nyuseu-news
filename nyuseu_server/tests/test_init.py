import pytest
from starlette.config import Config

settings = Config('.env')


@pytest.mark.asyncio
async def test_envfile():

    assert (settings('NYUSEU_SERVER_DEBUG'))
    assert settings("NYUSEU_SERVER_PORT")
    assert settings("NYUSEU_DATABASE_URL")
    assert settings("BYPASS_BOZO")
    assert settings("TIME_ZONE")
