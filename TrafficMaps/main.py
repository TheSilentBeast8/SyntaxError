import webapp2
from google.appengine.api import urlfetch
import json
import jinja2
import os
import urllib
from urlparse import urlparse
from datetime import datetime
import pytz
#import requests
#import httplib2 as http

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    # def get(self):
    #     welcome_template = the_jinja_env.get_template('templates/index.html')
    #     self.response.write(welcome_template.render())

    def get(self):

        welcome_template = the_jinja_env.get_template('templates/traffic.html')
        # stopName = self.request.get("stopid")
        #Authentication parameters
        headers = { 'AccountKey' : 'PZ7R2qzGS9KP2AhLyq5Bkw==',
        'accept' : 'application/json'} #this is by default

        #API parameters
        endpointUrl = 'http://datamall2.mytransport.sg/ltaodataservice/TrafficIncidents' #Resource URL
        #Build query string & specify type of API call
        response = urlfetch.fetch(endpointUrl,headers=headers)

        content = response.content

        response_as_json = json.loads(content)
        type = []
        details = []
        # print(response_as_json)
        incidents = response_as_json['value']
        for data in incidents:
            if data['Type'] == 'Roadwork':
                continue
            else:
                type.append(str(data['Type']))
                details.append(str(data['Message']))
        if len(type) == 0:
            x = 'There are no traffic accidents currently!'
            details.append(x)

        info = {'type': type,
                'details': details
                }










        self.response.write(welcome_template.render(info))



app = webapp2.WSGIApplication([
    ('/', MainHandler)

], debug=True)
