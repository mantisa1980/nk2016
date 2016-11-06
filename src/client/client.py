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
        #!! todo: put url in shell environment
        self.url='http://localhost:8888'
        self.access_token = '123'

    def login_by_guest(self):
        # TODO  check if user info cache exists. If exists, get previous user id. Otherwise, create one
        user_id = ''
        user_key = ''
        payload = {'from_type':'guest', 'user_id':user_id, 'user_key': user_key}
        r = requests.post('{}/login'.format(self.url), data=json.dumps(payload))
        print "[login response]:content=", r.content, " status code=", r.status_code, "header=", r.headers

        if r.status_code == 200:
            resp = json.loads(r.content)
            self.user_id = resp['user_id']
            self.user_key = resp['user_key']
            self.nickname = resp['nickname']
            #self.logger.debug("login ok! user_id={},key={},nickname={}".format(self.user_id,self.user_key, self.nickname))
            print "[login]: content=", r.content, " status code=", r.status_code, "header=", r.headers

    def auth(self):
        user_id = ''
        user_key = ''
        payload = {'user_id':self.user_id, 'user_key':self.user_key}
        r = requests.post('{}/auth'.format(self.url), data=json.dumps(payload))
        print "[auth response]:content=", r.content, " status code=", r.status_code, "header=", r.headers

        if r.status_code == 200:
            resp = json.loads(r.content)
            self.access_token = resp['access_token']
            self.expire = resp['expiration']

    def get_question(self):
        r = requests.get('{}/question?access_token={}&count={}'.format(self.url ,self.access_token , 10))
        #r = requests.get('{}/question?&count={}'.format(self.url ,self.access_token , 10))
        print "[get question]: content=", r.content, " status code=", r.status_code, "header=", r.headers
        if r.status_code == 200:
            resp = json.loads(r.content)
            self.serial_number = resp['serial_number']

    def commit_question(self):
        user_id = ''
        user_key = ''
        payload = {
            'access_token':self.access_token,
            'serial_number':self.serial_number,
            'answers':[
                { 'qid':0, 'answer':0 },
                { 'qid':2, 'answer':2 },
            ]
        }
        r = requests.post('{}/question'.format(self.url), data=json.dumps(payload))
        print "[commit question]:content=", r.content, " status code=", r.status_code, "header=", r.headers

        if r.status_code == 200:
            print "-------- testing duplicate questionniare"
            r = requests.post('{}/question'.format(self.url), data=json.dumps(payload))
            print "[re-commit question]:content=", r.content, " status code=", r.status_code, "header=", r.headers            
            pass



cli = NK2016Client()
cli.login_by_guest()
cli.auth()
cli.get_question()
cli.commit_question()

