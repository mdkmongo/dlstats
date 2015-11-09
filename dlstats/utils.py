# -*- coding: utf-8 -*-

import os

from dlstats import configuration
from dlstats import constants


def get_mongo_url():
    config = configuration['MongoDB'].copy()
    # TODO: configuration['MongoDB']['options']
    config['db'] = "widukind"
    default_url = "mongodb://%(host)s:%(port)s/%(db)s" % config
    return os.environ.get("DLSTATS_MONGODB_URL", default_url)


def get_es_url():
    default_url = "http://%(host)s:%(port)s" % configuration['ElasticSearch']
    return os.environ.get("DLSTATS_ES_URL", default_url)


def get_mongo_client(url=None):
    from pymongo import MongoClient
    # TODO: tz_aware
    url = url or get_mongo_url()
    client = MongoClient(url)
    return client


def get_mongo_db(url=None):
    from pymongo import MongoClient
    # TODO: tz_aware
    url = url or get_mongo_url()
    client = get_mongo_client(url)
    return client.get_default_database()


def get_es_client(url=None):
    from elasticsearch import Elasticsearch
    from urllib.parse import urlparse
    url = url or get_es_url()
    url = urlparse(url)
    es = Elasticsearch([{"host": url.hostname, "port": url.port}])
    return es