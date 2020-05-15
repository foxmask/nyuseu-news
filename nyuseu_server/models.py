# coding: utf-8
"""
   Nyuseu Server - 뉴스 - Models
"""
import databases
import datetime
import orm
from starlette.config import Config
import sqlalchemy

metadata = sqlalchemy.MetaData()
config = Config('.env')
DATABASE_URL = config('NYUSEU_DATABASE_URL')
database = databases.Database(DATABASE_URL, force_rollback=True)


class Folders(orm.Model):
    __tablename__ = "folders"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    title = orm.String(max_length=255, unique=True)
    date_created = orm.DateTime(default=datetime.datetime.now)
    date_modified = orm.DateTime(default=datetime.datetime.now)


class SourceFeeds(orm.Model):
    __tablename__ = "source_feeds"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    folder = orm.ForeignKey(Folders)
    title = orm.String(max_length=255, unique=True)
    url = orm.Text(max_length=255)
    date_created = orm.DateTime(default=datetime.datetime.now)
    date_modified = orm.DateTime(default=datetime.datetime.now)
    date_grabbed = orm.DateTime(default=datetime.datetime.now)
    status = orm.Boolean(default=True)


class Articles(orm.Model):
    __tablename__ = "articles"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    source_feeds = orm.ForeignKey(SourceFeeds)
    title = orm.String(max_length=255)
    text = orm.Text()
    date_created = orm.DateTime(default=datetime.datetime.now)
    read = orm.Boolean(default=False)


# Bootstrap
if __name__ == '__main__':
    # Create the database
    print("Nyuseu Server - 뉴스 - database creation")
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    print("Nyuseu Server - 뉴스 - done!")
