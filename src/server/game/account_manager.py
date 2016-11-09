#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"

import md5
import time
import traceback
import pymongo
from lib import log
import random


class AccountManager(object):
    def __init__(self,mongo_manager,redis_manager):
        self.mongo_manager = mongo_manager
        self.db_user = self.mongo_manager.get_database("User")
        self.col_serial = self.db_user["SerialNumber"]
        self.col_account = self.db_user["Account"]
        self.col_account.create_index([('account',pymongo.ASCENDING),('key',pymongo.ASCENDING)],unique=True)
        self.col_account.create_index([('score',pymongo.DESCENDING),('account',pymongo.ASCENDING)])

        self.TOKEN_EXPIRE_TIME = 3600
        self.redis_cli = redis_manager.get_redis_client('access_token')

    def generate_access_token(self,user_id):
        try:
            access_token = '{}_{}'.format(user_id, str(md5.new(str(random.randint(0,1000000))).hexdigest()))
            self.redis_cli.setex(access_token, self.TOKEN_EXPIRE_TIME, user_id)
            return access_token,self.TOKEN_EXPIRE_TIME
        except:
            log.error(traceback.format_exc())
            return None,None

    def validate_access_token(self,access_token):
        r = self.redis_cli.expire(access_token,self.TOKEN_EXPIRE_TIME)
        if r:
            user_id = access_token.split("_")[0]
            return True,user_id
        return False,None

    def create_account(self,nickname=None):
        try:
            doc = self.col_serial.find_and_modify({'name':'counter'}, {'$inc':{'value':1}},upsert=True,new=True)
            acc = '%08d' % doc['value']
            name = nickname if nickname is not None else acc
            key = str(md5.new(str(random.randint(0,1000000000))).hexdigest())
            self.col_account.insert({'account':acc,'key':key, 'score':0, 'nickname':name })
            return acc, key
        except:
            log.error(traceback.format_exc())
            return None,None

    def validate_account(self,user_id,user_key):
        try:
            doc = self.col_account.find_one({'account':user_id,'key':user_key })
            if doc is not None:
                return True
            return False 
        except:
            log.error(traceback.format_exc())
            return None

    def add_score(self,user_id,score):
        try:
            self.col_account.find_and_modify({'account':user_id}, {'$inc':{'score':score}})
        except:
            log.error(traceback.format_exc())

    def get_user_rank(self,user_id):
        try:
            doc = self.col_account.find_one({'account':user_id})
            score = doc['score']
            rank = self.col_account.find({'score':{'$gt':score}}).count()
            return doc, rank+1
        except:
            log.error(traceback.format_exc())

    def get_top_rank(self,count):
        ret = []
        try:
            cursor = self.col_account.find({},{"_id":False, "key":False}).sort([("score",pymongo.DESCENDING)]).limit(count)
            for i in cursor:
                doc = {
                    'user_id':i['account'],
                    'score':i['score'],
                    'nickname':i['nickname']
                }
                ret.append(doc)
        except:
            log.error(traceback.format_exc())
        
        return ret



