#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"

import falcon
import json
from handler import *
from database.mongo_manager import MongoManager
import gevent
from gevent import monkey;monkey.patch_all();


class ApplicationManager(object):
    def __init__(self):
        self.mongo_manager = MongoManager("mongo", 27017)

    def get_mongo_manager(self):
        return self.mongo_manager

ap_manager = ApplicationManager()
api_router = falcon.API()
api_router.add_route('/', default.DefaultWSGIHandler(ap_manager))
api_router.add_route('/login', login.LoginAPIHandler(ap_manager))

