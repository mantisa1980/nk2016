#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"
import requests
import json 
import os


class Logger(object):
    def debug(self,msg):
        print "[DEBUG]{}".format(msg)

    def info(self,msg):
        print "[INFO]{}".format(msg)

    def error(self,msg):
        print "[ERROR]{}".format(msg)


class NK2016Client(object):
    def __init__(self):
        self.logger = Logger()
        self.user_id = None
        self.user_key = None

    def login_by_guest(self):
        # TODO  check if user info cache exists. If exists, get previous user id. Otherwise, create one
        user_id = ''
        user_key = ''
        payload = {'from_type':'guest', 'user_id':user_id, 'user_key': user_key}
        r = requests.post('http://localhost:8888/login', data=json.dumps(payload))
        print "response=", r.content, " status code=", r.status_code, "header=", r.headers

        if r.status_code == 200:
            resp = json.loads(r.content)
            self.user_id = resp['user_id']
            self.user_key = resp['user_key']
            self.nickname = resp['nickname']
            self.logger.debug("login ok! user_id={},key={},nickname={}".format(self.user_id,self.user_key, self.nickname))


cli = NK2016Client()
cli.login_by_guest()