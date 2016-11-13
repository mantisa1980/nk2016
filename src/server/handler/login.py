#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"


from base import BaseWSGIHandler
import json

import falcon
import random
import md5
import time
import traceback
import pymongo
from lib import log

'''
Motivation: to get a unique game account.
If account(user_id and user_key) already saved in client side, just continue to auth.
'''

class LoginAPIHandler(BaseWSGIHandler):
    def __init__(self,ap_manager):
        super(LoginAPIHandler, self).__init__(ap_manager)
        self.account_mgr = ap_manager.get_account_manager()

    def handle_post(self,req,resp,data):
        if data['from_type'] == 'guest':
            return self.on_guest_login(resp,data)
        elif data['from_type'] == 'fb':
        	return self.on_facebook_login(resp,data)

    def on_guest_login(self,resp,data):
        account,key,name = self.account_mgr.create_account()
        return {'user_id':account, 'user_key':key, 'nickname':name}

    def on_facebook_login(self,resp,data):
    	fb_id = data['from_fb_info']['fb_id']
    	name = data['from_fb_info']['nickname']
    	bind_user_id = self.account_mgr.get_user_id_by_facebook(fb_id)
    	if bind_user_id is None:
        	account,key,nickname = self.account_mgr.create_account(name)
        	self.account_mgr.bind_user_id_by_facebook_id(account,fb_id)
        else:
        	account = bind_user_id
        	user_account_data = self.account_mgr.get_account(bind_user_id)
        	nickname = user_account_data['nickname']
        	key = user_account_data['key']
        
        return {'user_id':account, 'user_key':key, 'nickname':nickname}

