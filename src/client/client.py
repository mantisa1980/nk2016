#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "duyhsieh"
import requests
import json 

payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post('http://localhost:8888/login', data=json.dumps(payload))
print "response=", r.content, " status code=", r.status_code
