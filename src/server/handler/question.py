#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"


from base import CommandWSGIHandler
import random
import time
import traceback


class Question(object):
    def __init__(self,qid,title,options,answer):
        self.qid = qid
        self.title = title
        self.options = options
        self.answer = answer


class QuestionAPIHandler(CommandWSGIHandler):
    def __init__(self,ap_manager):
        super(QuestionAPIHandler, self).__init__(ap_manager)
        self.account_mgr = ap_manager.get_account_manager()
        self.question_manager = ap_manager.get_question_manager()
       
    def handle_get(self,req,resp,user_data,data):
        questions, no = self.question_manager.generate_questionnaire(user_data['user_id'])
        return {'questions': questions , 'serial_number':no }

    def handle_post(self,req,resp,user_data,cmd_data):
        b,score, result = self.question_manager.commit_questionnaire(user_data['user_id'],cmd_data )
        if b:
            return {'score':score,'result':result }