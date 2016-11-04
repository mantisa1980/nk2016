#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"


from base import CommandWSGIHandler
import random
import time
import traceback


class QuestionAPIHandler(CommandWSGIHandler):
    def __init__(self,ap_manager):
        super(QuestionAPIHandler, self).__init__(ap_manager)
        self.mongo_manager = ap_manager.get_mongo_manager()
        self.db_question = self.mongo_manager.get_database("Question")
        self.col_question = self.db_question["General"]
        self.answers = {
            0:0,
            1:1,
            2:2,
            3:3
        }

    def handle_get(self,req,resp,data):
        questions = [
            {'qid':0,'title':u'Author\'s name ?', 'options':[u'Lin',u'Hsieh',u'Jump',u'Da']},
            {'qid':2,'title':u'my name ?', 'options':[u'1',u'2',u'3',u'4']}
        ]
        return {'questions':questions }

    def handle_post(self,req,resp,data):
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

        return {'score':score, 'result':result }
