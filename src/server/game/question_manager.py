#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"

import md5
import time
import traceback
import pymongo
from lib import log
import random


class QuestionManager(object):
    def __init__(self,mongo_manager,redis_manager,account_manager):
        self.account_mgr = account_manager
        self.db_question = mongo_manager.get_database("Question")
        self.col_question = self.db_question["General"]
        self.col_question.create_index([('qid',pymongo.ASCENDING)],unique=True)
        self.redis_cli = redis_manager.get_redis_client('questionnaire')
        
        self.QUESTIONNAIRE_EXPIRE = 3600
        self.answers = {
            0:0,
            1:1,
            2:2,
            3:3
        }

    def generate_questionnaire(self,user_id):
        try:
            serial = str(md5.new(str(random.randint(0,1000000))).hexdigest())    
            questions = [
                {'qid':0,'title':u'Author\'s name ?', 'options':[u'Lin',u'Hsieh',u'Jump',u'Da']},
                {'qid':2,'title':u'my name ?', 'options':[u'1',u'2',u'3',u'4']}
            ]
            self.redis_cli.setex('{}:{}'.format(user_id,serial), self.QUESTIONNAIRE_EXPIRE, 0)
            return questions, serial
        except:
            log.error(traceback.format_exc())
            return None,None

    def commit_questionnaire(self,user_id,cmd_data):
        serial = cmd_data['serial_number']
        questionnaire_cache = self.redis_cli.get('{}:{}'.format(user_id,serial))
        if questionnaire_cache is None:
            return False, None,None
        elif str(questionnaire_cache) == '1':
            return False, None,None

        self.redis_cli.delete('{}:{}'.format(user_id,serial))

        user_answers = cmd_data['answers']
        result = []
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

        self.account_mgr.add_score(user_id,score)
        return True, score, result
