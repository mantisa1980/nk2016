#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class DefaultWSGIHandler(object):
    def __init__(self,server):
        self.server = server
        self.show_attributes = ['headers',
                                'protocol',
                                'method',
                                'host',
                                'subdomain',
                                'app',
                                'access_route',
                                'remote_addr',
                                'context',
                                'content_type', 
                                'cookies',
                                'params' # for http parameters
                                ]

    def show_attributes(self,req):
        for att in self.show_attributes:
            print "{}={}".format(att,getattr(req,att))

    def on_post(self, req, resp):
        response = {
            'handler': self.__class__.__name__
        }
        self.show_attributes(req)
        print "stream={}".format(req.stream.read())
        resp.body = json.dumps(response)

    def on_get(self, req, resp):
        response = {
            'handler': self.__class__.__name__
        }
        self.show_attributes(req)
        resp.body = json.dumps(response)    

    def on_put(self, req, resp):
        response = {
            'handler': self.__class__.__name__
        }
        self.show_attributes(req)
        print "stream={}".format(req.stream.read())
        resp.body = json.dumps(response)

    def on_delete(self, req, resp):
        response = {
            'handler': self.__class__.__name__
        }
        self.show_attributes(req)
        print "stream={}".format(req.stream.read())
        resp.body = json.dumps(response)
