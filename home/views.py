# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render
from google.cloud import storage
from home.models import *
import logging
import os

if not isLocal():
    import requests_toolbelt.adapters.appengine
    requests_toolbelt.adapters.appengine.monkeypatch()

BUCKET_NAME = 'helloworld-bucket1'


def index(request):
    try:
        if request.method == 'POST':
            task = request.POST.get('task', '')
            file = request.FILES['myfile']
            print(file.name)
            file_url = save_file(file)
            create_todo_model(task, file_url)
            print(file_url)

            todos = get_all_todos()
            return render(request, 'todo.html', {
                'todos': todos,
            })
    except Exception as e:
        logging.error(e.message)
        return HttpResponse("Hello world!")


def save_file(file):
    # Works anywhere on appengine, localhost and other platforms
    logging.debug('saving image')
    # Locate credentials file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_credentials_path = dir_path + '/mycred.json'

    # Create storage client instance
    client = storage.Client.from_service_account_json(json_credentials_path)
    bucket = client.get_bucket(BUCKET_NAME)

    # Save file and make it public
    try:
        blob = bucket.blob(file.name)
        blob.upload_from_file(ContentFile(file.read()))
        blob.make_public()
    except Exception as e:
        logging.error(e.message)
    return blob.public_url


def save_file_no_cred(file):
    # Works only on appengine
    logging.debug('saving image')
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(file.name)
    blob.upload_from_string(file.read())
    blob.make_public()
    return blob.public_url
