#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from definition import status_code as SC
import falcon
import random
import md5
import time
import traceback


class BaseWSGIHandler(object):
    def __init__(self,ap_manager):
        self.ap_manager = ap_manager

    def handle_get(self,req, resp, data):
        raise Exception('handle_get method not implemented!class={}'.format(x.__class__.__name__))

    def handle_post(self,req, resp, data):
        raise Exception('handle_post method not implemented!class={}'.format(x.__class__.__name__))

    def on_get(self, req, resp):
        resp.set_header('content-type', 'application/json')
        json_data = req.params

        ret = self.handle_get(req,resp,json_data)
        if type(ret) == dict:
            ret['status'] = SC.STATUS_OK
            resp.body = json.dumps(ret)
        else:
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'status':SC.STATUS_ERROR})

    def on_post(self, req, resp):
        resp.set_header('content-type', 'application/json')
        json_data = json.loads(req.stream.read())
        
        ret = self.handle_post(req,resp,json_data)
        if type(ret) == dict:
            ret['status'] = SC.STATUS_OK
            resp.body = json.dumps(ret)
        else:
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'status':SC.STATUS_ERROR})


class CommandWSGIHandler(BaseWSGIHandler):
    def __init__(self,ap_manager):
        self.ap_manager = ap_manager
        self.account_manager = ap_manager.get_account_manager()

    def get_user_by_token(self,token):
        boolean , user = self.account_manager.validate_access_token(token)
        if boolean:
            return user
        return None

    def on_get(self, req, resp):
        resp.set_header('content-type', 'application/json')
        json_data = req.params

        if 'access_token' not in json_data:
            resp.body = json.dumps({'status':SC.STATUS_INVALID_PARAMETER })
            resp.status = falcon.HTTP_400
            return

        user = self.get_user_by_token(json_data['access_token'])
        if user is None:
            resp.body = json.dumps({'status':SC.STATUS_TOKEN_EXPIRED })
            resp.status = falcon.HTTP_401
            return
    
        ret = self.handle_get(req,resp,{'user_id':user},json_data)
        if type(ret) == dict:
            ret['status'] = SC.STATUS_OK
            resp.body = json.dumps(ret)
        else:
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'status':SC.STATUS_ERROR})

    def on_post(self, req, resp):
        resp.set_header('content-type', 'application/json')
        json_data = json.loads(req.stream.read())
        
        if 'access_token' not in json_data:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'status':SC.STATUS_INVALID_PARAMETER })
            return

        user = self.get_user_by_token(json_data['access_token'])
        if user is None:
            resp.body = json.dumps({'status':SC.STATUS_TOKEN_EXPIRED })
            resp.status = falcon.HTTP_401
            return

        ret = self.handle_post(req,resp,{'user_id':user},json_data)
        if type(ret) == dict:
            ret['status'] = SC.STATUS_OK
            resp.body = json.dumps(ret)
        else:
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'status':SC.STATUS_ERROR})
