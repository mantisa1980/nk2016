#!/usr/bin/env python         
# -*- coding: 
__author__ = "duyhsieh"

import gevent
from gevent import monkey;monkey.patch_all();
import falcon
import json
from handler import *
from database.mongo_manager import MongoManager
from database.redis_manager import RedisManager
from game.account_manager import AccountManager
from game.question_manager import QuestionManager
from lib import log


class ApplicationManager(object):
    def __init__(self):
        self.mongo_manager = MongoManager()
        self.redis_manager = RedisManager()
        self.account_manager = AccountManager(self.mongo_manager,self.redis_manager)
        self.question_manager = QuestionManager(self.mongo_manager,self.redis_manager,self.account_manager)

    def get_mongo_manager(self):
        return self.mongo_manager

    def get_redis_manager(self):
        return self.redis_manager

    def get_account_manager(self):
        return self.account_manager

    def get_question_manager(self):
        return self.question_manager

ap_manager = ApplicationManager()
api_router = falcon.API()
api_router.add_route('/', default.DefaultWSGIHandler(ap_manager))
api_router.add_route('/login', login.LoginAPIHandler(ap_manager))
api_router.add_route('/auth', auth.AuthAPIHandler(ap_manager))
api_router.add_route('/question', question.QuestionAPIHandler(ap_manager))
api_router.add_route('/rank', rank.RankAPIHandler(ap_manager))
