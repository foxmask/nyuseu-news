# Nyuseu Server

!Nyuseu](https://raw.githubusercontent.com/foxmask/nyuseu-news/master/home.png)

## Prerequisites

Python 3.7+

```commandline
cd nyuseu_server
```

##  :wrench: Settings
copy the sample config file 
```
cp env.sample .env
```
and set the following values
```ini
# running in debug mode or not ?
NYUSEU_SERVER_DEBUG = False
# listen port number
NYUSEU_SERVER_PORT = 8001
NYUSEU_DATABASE_URL = driver://user:pass@localhost/dbname  # sqlite:///path/to/db.sqlite3
```

## :dvd: Database
create the database as follow 
```commandline
python models.py
Nyuseu Server - 뉴스 - database creation
Nyuseu Server - 뉴스 - done!
```

## :mega: Running the Server
start the server as follow 
```commandline
python server.py
Nyuseu Server - 뉴스 - Feeds Reader Server - Starlette powered
```

### :eyes: Importing OPML file
enter the following command
```commandline
python opml_load.py /path/to/the/file.opml
```
eg
```commandline
python opml_load.py ~/Download/feedly-e2343e92-9e71-4345-b045-cef7e1736cd2-2020-05-14.opml 
Nyuseu Server - 뉴스 - Feeds Reader Server - Starlette powered
Humor Le blog d'un odieux connard
Dev Vue.js News
Dev Real Python
Dev PyCharm Blog
Dev Python Insider
Dev The Django weblog
Dev Ned Batchelder's blog
Dev Pythonic News: Latest
Dev Caktus Blog
Dev The Official Vue News
Android Les Numériques
Android Frandroid
Dys Fédération Française des DYS
Gaming NoFrag
Gaming Gameblog
Gaming Gamekult - Jeux vidéo PC et consoles: tout l'univers des joueurs
Gaming PlayStation.Blog
Gaming jeuxvideo.com - PlayStation 4
Nyuseu Server - 뉴스 - Feeds Loaded
```

### :eyes: Running the Engine

Now we've imported OPML data, load the RSS Feeds by

```commandline
python engine.py
2020-05-15 15:31:49,892 - INFO - engine - Nyuseu Server Engine - 뉴스 - Feeds Reader Server - in progress
2020-05-15 15:31:50,697 - INFO - engine - Le blog d'un odieux connard: Entries created 0 / Read 10
2020-05-15 15:31:51,437 - INFO - engine - Vue.js News: Entries created 0 / Read 100
2020-05-15 15:31:52,751 - INFO - engine - Real Python: Entries created 0 / Read 30
2020-05-15 15:31:53,901 - INFO - engine - PyCharm Blog: Entries created 0 / Read 20
2020-05-15 15:31:53,988 - INFO - engine - Python Insider: Entries created 0 / Read 25
2020-05-15 15:31:54,053 - INFO - engine - The Django weblog: Entries created 0 / Read 10
2020-05-15 15:31:55,519 - INFO - engine - Ned Batchelder's blog: Entries created 0 / Read 10
2020-05-15 15:31:57,130 - INFO - engine - Pythonic News: Latest: Entries created 0 / Read 30
2020-05-15 15:31:58,013 - INFO - engine - Caktus Blog: Entries created 0 / Read 10
2020-05-15 15:31:59,051 - INFO - engine - The Official Vue News: Entries created 0 / Read 86
2020-05-15 15:31:59,140 - INFO - engine - Les Numériques: Entries created 0 / Read 40
2020-05-15 15:31:59,248 - INFO - engine - Frandroid: Entries created 0 / Read 15
2020-05-15 15:31:59,997 - INFO - engine - Fédération Française des DYS: Entries created 0 / Read 10
2020-05-15 15:32:00,706 - INFO - engine - NoFrag: Entries created 0 / Read 20
2020-05-15 15:32:01,060 - INFO - engine - Gameblog: Entries created 0 / Read 13
2020-05-15 15:32:01,650 - INFO - engine - Gamekult - Jeux vidéo PC et consoles: tout l'univers des joueurs: no feeds read
2020-05-15 15:32:01,711 - INFO - engine - PlayStation.Blog: Entries created 0 / Read 10
2020-05-15 15:32:02,197 - INFO - engine - jeuxvideo.com - PlayStation 4: Entries created 0 / Read 20
2020-05-15 15:32:02,198 - INFO - engine - Nyuseu Server Engine - 뉴스 - Feeds Reader Server - Finished!
```
