#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"
import requests
import json 
import os

convert_abcd = { 0:u'(0)',
                 1:u'(1)',
                 2:u'(2)',
                 3:u'(3)'  }

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
        self.url='http://54.174.128.174:8888'
        self.answers = []

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
            questions = resp['questions']
            print 'Questionnaire serial number:', self.serial_number
            qno = 1
            for i in questions:
                qid = i['qid']
                title = i['title'].encode('utf8')
                option_str = ''
                idx = 0
                for j in i['options']:
                    option_str = ' '.join([option_str , convert_abcd[idx] , j])
                    idx+=1
                option_str = option_str.encode('utf8')
                print 'No.{}:QID={} Title={} Options={}'.format(qno,qid,title,option_str)
                self.answers.append({"qid":qid })
                qno+=1

            s = raw_input("Please input answers separated by space(ex. 0 0 1 1 2 2 0 1 0 1)\n")
            tokens = s.split(" ")
            for i in range(0, len(tokens)):
                self.answers[i]["answer"] = int(tokens[i])

    def commit_question(self):
        user_id = ''
        user_key = ''
        payload = {
            'access_token':self.access_token,
            'serial_number':self.serial_number,
            'answers': self.answers
        }
        #print "commit:payload=", payload
        r = requests.post('{}/question'.format(self.url), data=json.dumps(payload))
        print "[commit question]:content=", unicode(r.content), " status code=", r.status_code, "header=", r.headers

        if r.status_code == 200:
            resp = json.loads(r.content)
            result = resp['result']
            print 'Questionnaire result: score=', resp['score']
            qno = 1
            for i in result:
                qid = i['qid']
                title = i['title'].encode('utf8')
                option_str = ''
                idx = 0
                for j in i['options']:
                    option_str = ' '.join([option_str , convert_abcd[idx] , j])
                    idx+=1
                option_str = option_str.encode('utf8')
                print 'No.{} Correct:{} YourAns:{} QID={} Title={} Options={}'.format(qno,i['correct'],i['your_answer'],qid,title,option_str)
                qno+=1

            #print "-------- testing duplicate questionniare"
            #r = requests.post('{}/question'.format(self.url), data=json.dumps(payload))
            #print "[re-commit question]:content=", r.content, " status code=", r.status_code, "header=", r.headers            
            pass

    def get_rank(self):
        r = requests.get('{}/rank?access_token={}&user_id={}&count={}'.format(self.url, self.access_token ,self.user_id , 10))
        print '[get rank]: content=', r.content, ' status code=', r.status_code, 'header=', r.headers
        if r.status_code == 200:
            resp = json.loads(r.content)
            print 'your rank', resp['rank'], " your score:", resp['score']
            print 'top ranks'
            for i in resp['top_rank']:
                print 'user_id:{},nickname:{},score:{}'.format(i['user_id'], i['nickname'], i['score'])



cli = NK2016Client()
cli.login_by_guest()
cli.auth()
cli.get_question()
cli.commit_question()
cli.get_rank()

