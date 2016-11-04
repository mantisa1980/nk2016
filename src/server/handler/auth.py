#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"


from base import BaseWSGIHandler
import json
from definition import status_code as SC
import falcon
import random
import md5
import time
import traceback
import pymongo
import redis


class AuthAPIHandler(BaseWSGIHandler):
    def __init__(self,ap_manager):
        super(AuthAPIHandler, self).__init__(ap_manager)
        self.account_mgr = ap_manager.get_account_manager()

    def handle_post(self,req,resp,data):
        if self.account_mgr.validate_account(data['user_id'],data['user_key']):
        	token,expire = self.account_mgr.generate_access_token(data['user_id'])
        	if token != None and expire != None:
        		return {'access_token':token, 'expiration':expire}
        