#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"
import redis


class RedisManager(object):
    def __init__(self):
    	self.redis_list = {
    		"access_token":redis.StrictRedis(host='redis', port=6379,db=0)
    	}

    def get_redis_client(self,dbname):
    	return self.redis_list[dbname]
