#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"


from base import BaseWSGIHandler
import json
from definition import status_code as SC
import falcon
import random


class LoginAPIHandler(BaseWSGIHandler):
    def __init__(self,ap_manager):
        self.mongo_manager = ap_manager.get_mongo_manager()
        self.db_user = self.mongo_manager.get_database("User")
        ##!! TODO create index


    def check_post_parameter(self,data):
        if 'from_type' not in data:
            return False

        #!! TODO: check FB, Email.
        return True

    def on_post(self, req, resp):
        check_param, data = super(LoginAPIHandler, self).on_post(req, resp)
        if not check_param:
            response = {'status':SC.STATUS_INVALID_PARAMETER }
            resp.status = falcon.HTTP_400
            return

        if data['from_type'] == 'guest':
            self.on_guest_login(resp,data)

        

    def on_guest_login(self,resp,data):
        account,key = self.create_account()
        response = {'user_id':account, 'user_key':key, 'nickname':account}
        resp.body = json.dumps(response)
        resp.status = falcon.HTTP_200

    def create_account(self):
        #!!
        return random.randint(0,1000), random.randint(0,1000000)

