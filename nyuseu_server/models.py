# coding: utf-8
"""
   Nyuseu Server - 뉴스 - Models
"""

import databases
import datetime
import orm
import os
import sys

from nyuseu_server import settings

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_FOLDER = os.path.dirname(PROJECT_DIR)
sys.path.append(PARENT_FOLDER)

database = databases.Database(settings.NYUSEU_DATABASE_URL, force_rollback=True)
models = orm.ModelRegistry(database=database)


class Folders(orm.Model):

    tablename = "folders"
    registry = models

    fields = {
        "id": orm.Integer(primary_key=True),
        "title": orm.String(max_length=255, unique=True),
        "date_created": orm.DateTime(default=datetime.datetime.now),
        "date_modified": orm.DateTime(default=datetime.datetime.now),
    }


class Feeds(orm.Model):

    tablename = "feeds"
    registry = models

    fields = {
        "id": orm.Integer(primary_key=True),
        "folder": orm.ForeignKey(Folders),
        "title": orm.String(max_length=255, unique=True),
        "url": orm.Text(max_length=255),
        "date_created": orm.DateTime(default=datetime.datetime.now),
        "date_modified": orm.DateTime(default=datetime.datetime.now),
        "date_grabbed": orm.DateTime(default=datetime.datetime.now),
        "status": orm.Boolean(default=True),
    }


class Articles(orm.Model):

    tablename = "articles"
    registry = models

    fields = {
        "id": orm.Integer(primary_key=True),
        "feeds": orm.ForeignKey(Feeds),
        "title": orm.String(max_length=255, unique=True),
        "image": orm.Text(allow_null=True),
        "source_url": orm.Text(allow_null=True),
        "text": orm.Text(),
        "date_created": orm.DateTime(default=datetime.datetime.now),
        "read": orm.Boolean(default=False),
        "read_later": orm.Boolean(default=False),
    }


# Bootstrap
if __name__ == '__main__':
    print("Nyuseu Server - 뉴스 - database creation")
    # Create the database
    print(f"database creation {settings.NYUSEU_DATABASE_URL}")
    # Create the tables
    models.create_all()
    print("Nyuseu Server - 뉴스 - done!")
