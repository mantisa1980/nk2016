#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"

import falcon
import json
from handler import *
from database.mongo_manager import MongoManager
import gevent
from gevent import monkey;monkey.patch_all();


class NK2016Server(falcon.API):
    def __init__(self):
        falcon.API.__init__(self)
        self.mongo_manager = MongoManager("mongo", 27017)

    def get_mongo_manager(self):
        return self.mongo_manager


nk2016server = NK2016Server()
nk2016server.add_route('/', default.DefaultWSGIHandler(nk2016server))
nk2016server.add_route('/login', login.LoginAPIHandler(nk2016server))

