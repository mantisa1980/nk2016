#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class BaseWSGIHandler(object):
    def __init__(self,server):
        self.server = server

    def check_get_parameter(self,data):
        #req.get_param(key)
        return True

    def check_post_parameter(self,data):
        return True

    def on_post(self, req, resp):
        resp.set_header('content-type', 'application/json')
        json_data = json.loads(req.stream.read())
        return self.check_post_parameter(json_data), json_data

    def on_get(self, req, resp):
        resp.set_header('content-type', 'application/json')
        json_data = json.loads(req.stream.read())
        return self.check_get_parameter(json_data), json_data