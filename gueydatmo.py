import requests
import cherrypy
from datetime import datetime,timedelta

import random
import string
import os, os.path

class token:
    '''Handles Netatmo API token'''
    
    # hardcoded credentials
    client_id = "54ae5efd1c775977ffcc5697"
    client_secret = "sQNIHM5zlCRgEmN8xT7P5SIp4EKs4Zk7nIMkAsXoG9"
    username = "mottin@gueydan.eu"
    password = "mdpnetatmo"
    
    # url
    NetatmoAuthUrl = "http://api.netatmo.net/oauth2/token"
    
    def __init__(self):
        self.__tok = {}
    
    # Use to get token for netatmo API
    def getToken(self):
        if "deadline" not in self.__tok:
            self.__requestToken()
            return self.__tok["access_token"]
                        
        else:
            now = datetime.now()
            if now<self.__tok["deadline"]:
                return self.__tok["access_token"]
            else:
                self.__refreshToken()
                return self.__tok["access_token"]
                
        
    def __requestToken(self):
        now = datetime.now() 
        credentials = {}
        credentials["client_id"] = token.client_id
        credentials["client_secret"] = token.client_secret
        credentials["username"] = token.username
        credentials["password"] = token.password
        credentials["scope"] = "read_thermostat"
        credentials["grant_type"] = "password"

        r = requests.post(token.NetatmoAuthUrl,data=credentials)
        self.__tok = eval(r.text)
        duration = timedelta(seconds=int(self.__tok["expires_in"]))    
        deadline = now + duration
        self.__tok["deadline"] = deadline
        
    def __refreshToken(self):
        now = datetime.now() 
        credentials = {}
        credentials["client_id"] = token.client_id
        credentials["client_secret"] = token.client_secret
        credentials["grant_type"] = "refresh_token"
        credentials["refresh_token"] = self.__tok["refresh_token"]

        r = requests.post(token.NetatmoAuthUrl,data=credentials)
        self.__tok = eval(r.text)
        duration = timedelta(seconds=int(self.__tok["expires_in"]))    
        deadline = now + duration
        self.__tok["deadline"] = deadline

class GueydAtmo(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <img src="/static/logo.jpg" alt="logo" width="50">
            <form method="post" action="random">
              <input type="text" value="8" name="length" />
              <button type="submit">Give it now!</button>
            </form>
          </body>
        </html>"""
    
    @cherrypy.expose
    def random(self,length="8"):
        some_string =  ''.join(random.sample(string.hexdigits,int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string
    
    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

if __name__ == '__main__':
    root = {}
    root['tools.sessions.on'] = True
    root['tools.staticdir.root'] = os.path.abspath(os.getcwd())
    static = {}
    static['tools.staticdir.on'] = True
    static['tools.staticdir.dir'] = './web'
    conf = {}
    conf['/'] = root
    conf['/static'] = static

    cherrypy.quickstart(GueydAtmo(),'/',conf)