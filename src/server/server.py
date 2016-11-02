#!/usr/bin/env python         
# -*- coding: 
__author__ = "duyhsieh"

import falcon
import json
from handler import *
from database.mongo_manager import MongoManager
import gevent
from gevent import monkey;monkey.patch_all();

class Logger(object):
	def debug(self,msg):
		print "[DEBUG]{}".format(msg)
	def info(self,msg):
		print "[INFO]{}".format(msg)
	def error(self,msg):
		print "[ERROR]{}".format(msg)
	

class ApplicationManager(object):
    def __init__(self):
        self.logger = Logger()
        self.mongo_manager = MongoManager("mongo", 27017)

    def get_mongo_manager(self):
        return self.mongo_manager

    def get_logger(self):
    	return self.logger

ap_manager = ApplicationManager()
#print ap_manager.get_logger()
api_router = falcon.API()
api_router.add_route('/', default.DefaultWSGIHandler(ap_manager))
api_router.add_route('/login', login.LoginAPIHandler(ap_manager))
api_router.add_route('/question', question.QuestionAPIHandler(ap_manager))

