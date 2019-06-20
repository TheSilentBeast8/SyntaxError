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
    def get(self):
        welcome_template = the_jinja_env.get_template('templates/carpark.html')

        self.response.write(welcome_template.render())

    def post(self):
        with open('carparks_new.json') as data_file:
            data = json.load(data_file)
        welcome_template = the_jinja_env.get_template('templates/carpark.html')
        parkName = self.request.get("carpark")
        parkName_new = data[parkName]
        #Authentication parameters
        headers = { 'AccountKey' : 'PZ7R2qzGS9KP2AhLyq5Bkw==',
        'accept' : 'application/json'} #this is by default

        #API parameters
        endpointUrl = 'http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2' #Resource URL
        #Build query string & specify type of API call
        response = urlfetch.fetch(endpointUrl,headers=headers)

        content = response.content

        response_as_json = json.loads(content)



        #print(response_as_json)
        lots = ''

        details = response_as_json['value']
        for data in details:
            if data['Development'].lower() == parkName_new.lower():
                lots = str(data["AvailableLots"])
                content = 'Number of lots available at '+parkName+' : '
        print(lots)





        info = {
           "lots":lots,
           "parkName":parkName,
           "content": content
        }
        self.response.write(welcome_template.render(info))



app = webapp2.WSGIApplication([
    ('/', MainHandler)

], debug=True)
