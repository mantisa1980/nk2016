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
        self.QUEST_COUNT = 10
        
        self.QUESTIONNAIRE_EXPIRE = 3600

    def generate_questionnaire(self,user_id):
        try:
            serial = str(md5.new(str(random.randint(0,1000000))).hexdigest())
            nos = {}
            max_q_count = self.col_question.count()

            counter = 0
            while counter < self.QUEST_COUNT and counter < max_q_count:
                rng = random.randrange(0,max_q_count)
                if rng not in nos:
                    nos[rng] = None
                    counter+=1

            cursor = self.col_question.find({"qid":{"$in":nos.keys()} },{"_id":0, "ans_idx":0 } )
            questions = []
            for i in cursor:
                questions.append(i)

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

        qids = [ x['qid'] for x in cmd_data['answers'] ] 
        #print "commit qids=", qids

        ref = {}
        cursor = self.col_question.find({"qid":{"$in":qids} },{"_id":0})
        for i in cursor:
            qid = i['qid']
            ref[qid] = i

        result = []
        score = 0
        for x in cmd_data['answers']:
            qid = x['qid']
            ans = x['answer']
            doc = {
                'qid':qid,
                'title':ref[qid]['title'],
                'options':ref[qid]['options'],
                'your_answer':x['answer'],
                'correct': 1 if ref[qid]['ans_idx'] == ans else 0
            }
            if doc['correct'] == 1:
                score+=1
            result.append(doc)

        self.account_mgr.add_score(user_id,score)
        return True, score, result
