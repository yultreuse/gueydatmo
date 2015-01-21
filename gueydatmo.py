import requests
import cherrypy
from datetime import datetime,timedelta
import time,calendar

import os, os.path
import json

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
        self.__tok = json.loads(r.text)
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
        self.__tok = json.loads(r.text)
        duration = timedelta(seconds=int(self.__tok["expires_in"]))    
        deadline = now + duration
        self.__tok["deadline"] = deadline

class GueydAtmo(object):
        
    def __init__(self):
        self.__tok = token()
        
    def netAtmoAPI(self,url,params):
        params["access_token"] = self.__tok.getToken()
        ans = requests.post("http://api.netatmo.net/api" + url,data=params)
        dico = json.loads(ans.text)
        if "status" in dico:
            if "ok" == dico["status"] and "body" in dico:
                return dico["body"]
        return ans.text
    
    def getUTCEpochTime(self,t=None):
        #default t to beginning of current day
        if t is None:
            t=time.strptime(time.strftime("%Y-%m-%d",time.localtime()),"%Y-%m-%d")
        return calendar.timegm(t)
    
    @cherrypy.expose
    def index(self):
        token.cred = cherrypy.request.app.config['credentials']
        return file('web/index.html')
    
    @cherrypy.expose
    def devicelist(self):
        if "device" in cherrypy.session:
            print "device and module already in session"
        else:
            qryparams = {}
            qryparams["app_type"] = "app_thermostat"
            dico = self.netAtmoAPI("/devicelist", qryparams)
            cherrypy.session["device"] = dico["devices"][0]
            cherrypy.session["module"] = dico["modules"][0]
        return "device : " + cherrypy.session["device"]["_id"] + "<br>module : " + cherrypy.session["module"]["_id"]

    
    @cherrypy.expose
    def getuser(self):
        if "user" in cherrypy.session:            
            print "user already in session"
        else:
            qryparams = {}
            cherrypy.session["user"]=self.netAtmoAPI("/getuser", qryparams)
        print cherrypy.session["user"]
        return cherrypy.session["user"]["mail"]
    
    @cherrypy.expose
    def getmeasure(self):
        qryparams = {}
        if "device" not in cherrypy.session:
            self.devicelist()
            
        # Build query
        qryparams["device_id"] = cherrypy.session["device"]["_id"]
        qryparams["module_id"] = cherrypy.session["module"]["_id"]
        qryparams["scale"] = "max"
        qryparams["date_begin"] = str(self.getUTCEpochTime()-3600)
        qryparams["type"] = "Temperature"
        qryparams["optimize"] = "false"
        dico = self.netAtmoAPI("/getmeasure", qryparams)
        
        # Parse output, sort by ascending order
        listVal = dico.items()
        listVal.sort()
        
        # Build data for plotting
        outVal = []
        for elem in listVal:
            tstamp = int(elem[0])
            tstring = time.strftime("%Y-%m-%d %I:%M%p",time.localtime(tstamp))
            outVal.append([tstring,elem[1][0]])
        
        return json.dumps(outVal)
    
    @cherrypy.expose
    def getthermstate(self):
        qryparams = {}
        if "device" not in cherrypy.session:
            self.devicelist()
        qryparams["device_id"] = cherrypy.session["device"]["_id"]
        qryparams["module_id"] = cherrypy.session["module"]["_id"]
        dico = self.netAtmoAPI("/getthermstate", qryparams)
        return str(dico)
     

if __name__ == '__main__':

    gueydAtmoApp = GueydAtmo()
    cherrypy.quickstart(gueydAtmoApp,'/',"gueydatmo.conf")