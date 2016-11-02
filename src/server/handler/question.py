#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"


from base import BaseWSGIHandler
import json
from definition import status_code as SC
import falcon
import random
import time
import traceback



class QuestionAPIHandler(BaseWSGIHandler):
    def __init__(self,ap_manager):
        self.mongo_manager = ap_manager.get_mongo_manager()
        self.db_question = self.mongo_manager.get_database("Question")
        self.col_question = self.db_question["General"]
        self.logger = ap_manager.get_logger()
        self.answers = {
            0:0,
            1:1,
            2:2,
            3:3
        }

        ##!! TODO create index

    def check_get_parameter(self,data):
        if 'access_token' in data and 'count' in data:
            return True
        return False

    def check_post_parameter(self,data):
        if 'access_token' in data and 'answers' in data:
            return True
        print "check fail,", data
        return False
        
    def on_get(self, req, resp):
        check_param, data = super(QuestionAPIHandler, self).on_get(req, resp)
        if not check_param:
            response = {'status':SC.STATUS_INVALID_PARAMETER }
            resp.status = falcon.HTTP_400
            return

        questions = [
            {'qid':0,'title':u'Author\'s name ?', 'options':[u'Lin',u'Hsieh',u'Jump',u'Da']},
            {'qid':2,'title':u'my name ?', 'options':[u'1',u'2',u'3',u'4']}
        ]

        response = {'status':SC.STATUS_OK, 'questions':questions }
        resp.body = json.dumps(response)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        check_param, data = super(QuestionAPIHandler, self).on_post(req, resp)
        if not check_param:
            response = {'status':SC.STATUS_INVALID_PARAMETER }
            resp.status = falcon.HTTP_400
            return

        user_answers = data['answers']
        result = []
        #!! todo: check index valid. replace title/options 
        score = 0
        for x in user_answers:
            qid = x['qid']
            ans = x['answer']
            doc = {
                'qid':x['qid'],
                'title':'question ' + str(qid),
                'options':['option1','option2','option3','option4'],
                'your_answer':x['answer'],
                'correct': 1 if self.answers[qid] == ans else 0
            }
            if self.answers[qid] == ans:
                score+=1
            result.append(doc)

        response = {'status':SC.STATUS_OK,
                    'score':score,
                    'result':result 
        }

        resp.body = json.dumps(response)
        resp.status = falcon.HTTP_200
