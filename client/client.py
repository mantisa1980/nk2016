import falcon
import json
 
class APIHandlerRoot(object):
    def __init__(self):
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

    def __show_attributes(self,req):
        for att in self.show_attributes:
            print "{}={}".format(att,getattr(req,att))

    def on_post(self, req, resp):
        response = {
            'method': 'post',
            'data': 'post data',
            'handler': self.__class__.__name__
        }
        self.__show_attributes(req)
        print "stream={}".format(req.stream.read())
        resp.body = json.dumps(response)

    def on_get(self, req, resp):
        """Handles GET requests"""
        response = {
            'method': 'get',
            'data': 'get data',
            'handler': self.__class__.__name__
        }
        self.__show_attributes(req)
        resp.body = json.dumps(response)    

    def on_put(self, req, resp):
        response = {
            'method': 'put',
            'data': 'put data',
            'handler': self.__class__.__name__
        }
        self.__show_attributes(req)
        print "stream={}".format(req.stream.read())
        resp.body = json.dumps(response)

    def on_delete(self, req, resp):
        response = {
            'method': 'delete',
            'data': 'delete data',
            'handler': self.__class__.__name__
        }
        self.__show_attributes(req)
        print "stream={}".format(req.stream.read())
        resp.body = json.dumps(response)

class APIHandlerApp1(APIHandlerRoot):
    pass

api = falcon.API()
api.add_route('/', APIHandlerRoot())
api.add_route('/app1', APIHandlerApp1())
