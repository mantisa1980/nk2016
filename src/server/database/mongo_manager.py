#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"
import pymongo


class MongoManager(object):
    def __init__(self, host, port):
    	self.mongo = pymongo.MongoClient(host=host, port=port)

    def get_database(self,dbname):
    	return self.mongo[dbname]
