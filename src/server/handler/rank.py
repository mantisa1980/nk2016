#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"
from base import CommandWSGIHandler
import random
import time
import traceback


class RankAPIHandler(CommandWSGIHandler):
    def __init__(self,ap_manager):
    	super(RankAPIHandler, self).__init__(ap_manager)
        self.account_mgr = ap_manager.get_account_manager()
        self.question_manager = ap_manager.get_question_manager()

    def handle_get(self,req,resp,user_data,cmd_data):
    	user_id = user_data['user_id']
    	count = cmd_data['count']
    	#print "user id", user_id, 'count', count
    	user_doc, rank = self.account_mgr.get_user_rank(user_id)
    	top_rank = self.account_mgr.get_top_rank(10)

        return {
        	'rank':rank,
        	'nickname':user_doc['nickname'],
        	'score':user_doc['score'],
        	'top_rank': top_rank
        }
