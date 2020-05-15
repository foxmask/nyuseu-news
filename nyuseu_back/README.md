# Nyuseu Server

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
NYUSEU_DEBUG = False
# number of feeds to get for each page
NYUSEU_PAGINATOR = 20
# host
NYUSEU_HOST = 127.0.0.1
# listen port number
NYUSEU_PORT = 8001
# BASE URL
NYUSEU_BASE_URL = '/'
```

## :mega: Running the BackEnd

```commandline
python app.py 
nyuseu - 뉴스 - Feeds Reader - Starlette powered
```