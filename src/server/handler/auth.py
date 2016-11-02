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



class AuthAPIHandler(BaseWSGIHandler):
    def __init__(self,ap_manager):
        self.logger = ap_manager.get_logger()

    def check_post_parameter(self,data):
        if 'user_id' in data and user_key in data:
            return True
        return False

    def on_post(self, req, resp):
        return False
