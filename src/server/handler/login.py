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

    def on_guest_login(self,resp,data):
        account,key = self.account_mgr.create_account()
        return {'user_id':account, 'user_key':key, 'nickname':account}
