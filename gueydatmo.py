import requests
import cherrypy
from datetime import datetime,timedelta

import os, os.path

class token:
    '''Handles Netatmo API token'''    
    cred = {}
    
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
        credentials["client_id"] = token.cred['client_id']
        credentials["client_secret"] = token.cred['client_secret']
        credentials["username"] = token.cred['username']
        credentials["password"] = token.cred['password']
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
        credentials["client_id"] = token.cred['client_id']
        credentials["client_secret"] = token.cred['client_secret']
        credentials["grant_type"] = "refresh_token"
        credentials["refresh_token"] = self.__tok["refresh_token"]

        r = requests.post(token.NetatmoAuthUrl,data=credentials)
        self.__tok = eval(r.text)
        duration = timedelta(seconds=int(self.__tok["expires_in"]))    
        deadline = now + duration
        self.__tok["deadline"] = deadline

class GueydAtmo(object):
        
    def __init__(self):
        self.__tok = token()
    
    @cherrypy.expose
    def index(self):
        token.cred = cherrypy.request.app.config['credentials']
        return file('web/index.html')
    
    @cherrypy.expose
    def devicelist(self):
        qryparams = {}
        qryparams["access_token"] = self.__tok.getToken()
        qryparams["app_type"] = "app_thermostat"
        ans = requests.post("http://api.netatmo.net/api/devicelist",data=qryparams)
        return ans.text 
    
    @cherrypy.expose
    def gaws(self,cmd):
        if cmd == "gettemp":
            qryparams = {}
            qryparams["access_token"] = self.__tok.getToken()
            qryparams["app_type"] = "app_thermostat"
            ans = requests.post("http://api.netatmo.net/api/devicelist",data=qryparams)
            return ans.text           

if __name__ == '__main__':

    gueydAtmoApp = GueydAtmo()
    cherrypy.quickstart(gueydAtmoApp,'/',"gueydatmo.conf")