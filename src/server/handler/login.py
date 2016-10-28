#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"


from default import DefaultWSGIHandler
import json
import pymongo


class LoginAPIHandler(DefaultWSGIHandler):
    def on_post(self, req, resp):
        response = {
            'handler': self.__class__.__name__
        }
        stream = req.stream.read()
        data = json.loads(stream)
        print "data=", data, type(data)
        self.server.get_mongo_manager().get_database("AAA")["BBB"].insert({"A":"B"}) #!!
        response = data
        resp.body = json.dumps(response)
