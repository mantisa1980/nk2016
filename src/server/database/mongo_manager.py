#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"
import pymongo


class MongoManager(object):
    def __init__(self):
    	self.mongo = pymongo.MongoClient(host='mongo', port=27017)

    def get_database(self,dbname):
    	return self.mongo[dbname]
