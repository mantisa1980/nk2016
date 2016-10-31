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

        ##!! TODO create index

    def check_get_parameter(self,data):
        #!!
        return True

    def check_post_parameter(self,data):
        #!!
        return True

    def on_get(self, req, resp):
        check_param, data = super(QuestionAPIHandler, self).on_get(req, resp)
        if not check_param:
            response = {'status':SC.STATUS_INVALID_PARAMETER }
            resp.status = falcon.HTTP_400
            return

        response = {'status':SC.STATUS_OK, 'questions':[{'qid':0,'title':'Author\'s name ?', 'options':['Lin','Hsieh','Jump','Da']}] }
        resp.body = json.dumps(response)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        check_param, data = super(QuestionAPIHandler, self).on_post(req, resp)
        if not check_param:
            response = {'status':SC.STATUS_INVALID_PARAMETER }
            resp.status = falcon.HTTP_400
            return

        response = {'status':SC.STATUS_OK, 'questions':[{'qid':0,'title':'Author\'s name ?', 'options':['Lin','Hsieh','Jump','Da']}] }
        resp.body = json.dumps(response)
        resp.status = falcon.HTTP_200
