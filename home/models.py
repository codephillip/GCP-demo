# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ae_hello_django.settings import isLocal
import datetime
import time

if not isLocal():
    from google.appengine.ext import ndb


class TodoModel(ndb.Model):
    task = ndb.StringProperty()
    created_at = ndb.DateTimeProperty()
    file_url = ndb.StringProperty(default='https://blogs.psychcentral.com/nlp/files/2016/06/getthhingsdone-300x300.jpg')
    done = ndb.BooleanProperty(default=False)

    @classmethod
    def query_model(cls):
        query = cls.query()
        return query.fetch()


def create_todo_model(task, file_url, done=False):
    print("create todo")
    id = datetime_in_millis()
    todo_key = ndb.Key(TodoModel, id)
    todo_model = TodoModel()
    todo_model.key = todo_key
    todo_model.task = task
    todo_model.file_url = file_url
    todo_model.created_at = datetime.datetime.utcnow()
    todo_model.done = done
    todo_model.put()


def get_all_todos():
    print("Get all todo")
    todo_models = TodoModel.query().fetch()
    print list(todo_models)
    return todo_models


def datetime_in_millis():
    return int(time.mktime(datetime.datetime.now().timetuple()) * 1000)
