# Nyuseu Front

## Prerequisites

Python 3.7+

```commandline
cd nyuseu_back
```

##  :wrench: Settings
copy the sample config file 
```
cp env.sample .env
```
and set the following values
```ini
# running in debug mode or not ?
NYUSEU_FRONT_DEBUG = False
# number of feeds to get for each page
NYUSEU_PAGINATOR = 20
# host
NYUSEU_FRONT_HOST = 127.0.0.1
# listen port number
NYUSEU_FRONT_PORT = 8003
# BASE URL
NYUSEU_FRONT_BASE_URL = '/'
NYEUSEU_HOST=http://127.0.0.1/
NYEUSEU_PORT=8002
```

## :mega: Running the FrontEnd

```commandline
python front.py 
Nyuseu Front - 뉴스 - Feeds Reader - Starlette powered
```
