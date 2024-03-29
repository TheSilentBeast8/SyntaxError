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
        welcome_template = the_jinja_env.get_template('templates/bustimings.html')
        headers = { 'AccountKey' : 'PZ7R2qzGS9KP2AhLyq5Bkw==',
        'accept' : 'application/json'} #this is by default

        #API parameters
        endpointUrl1 = 'http://datamall2.mytransport.sg/ltaodataservice/TrainServiceAlerts' #Resource URL
        #Build query string & specify type of API call
        response1 = urlfetch.fetch(endpointUrl1,headers=headers)

        content1 = response1.content

        response_as_json1 = json.loads(content1)
        print(response_as_json1)
        print(response_as_json1['value']['Status'])
        if response_as_json1['value']['Status'] == 1:
            train_message = 'Train service is as per normal now.'
        else:
            train_message = response_as_json1['value']['Message']


        train = {'train_message':train_message}
        self.response.write(welcome_template.render(train))

    def post(self):
        with open('busstops_new.json') as data_file:
            data = json.load(data_file)
        welcome_template = the_jinja_env.get_template('templates/bustimings.html')
        stopName = self.request.get("stopid")
        stopId = data[stopName]
        #Authentication parameters
        headers = { 'AccountKey' : 'PZ7R2qzGS9KP2AhLyq5Bkw==',
        'accept' : 'application/json'} #this is by default

        #API parameters
        endpointUrl = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode='+stopId #Resource URL
        #Build query string & specify type of API call
        response = urlfetch.fetch(endpointUrl,headers=headers)

        content = response.content

        response_as_json = json.loads(content)



        #print(response_as_json)
        time_zone = pytz.timezone('Asia/Singapore')

        timings = response_as_json['Services']
        busno_arr = []

        time_arr = []

        for service in timings:
            bustime1 = service['NextBus']["EstimatedArrival"]
            if bustime1 == '':
                continue
            bustime2 = service['NextBus2']["EstimatedArrival"]
            if bustime2 == '':
                continue
            standorseat1 = ''
            standorseat2 = ''
            if service['NextBus']["Load"] == 'SEA':
                standorseat1 = 'seating available!'
            else:
                standorseat1 = 'standing available.'

            if service['NextBus2']["Load"] == 'SEA':
                standorseat2 = 'seating available!'
            else:
                standorseat2 = 'standing available.'

            bustime1 = datetime.strptime(bustime1,"%Y-%m-%dT%H:%M:%S+08:00")
            bustime2 = datetime.strptime(bustime2,"%Y-%m-%dT%H:%M:%S+08:00")
            time_zone = pytz.timezone('Asia/Singapore')
            sgtime = datetime.now(time_zone)
            sgtime = sgtime.strftime("%Y-%m-%d %H:%M:%S")
            sgtime = datetime.strptime(sgtime,"%Y-%m-%d %H:%M:%S")
            timediff1 = bustime1 - sgtime
            timediff2 = bustime2 - sgtime
            timeinmin1 = divmod(timediff1.total_seconds(), 60)[0]
            time1 = str(timeinmin1)+' minutes. and there is '+standorseat1
            timeinmin2 = divmod(timediff2.total_seconds(), 60)[0]
            time2 = str(timeinmin2)+' minutes. and there is '+standorseat2
            if timeinmin1<=0:
                time1 = 'Arriving!'
            x = ''
            x = ' will be coming in: '+time1+' Subsequent timing: '+time2
            time_arr.append(x)
            busno_arr.append(service['ServiceNo'])
        print(time_arr)



        info = {
           "timings":time_arr,
           "busno": busno_arr,
           "stopid": stopName
        }
        self.response.write(welcome_template.render(info))
        busno_arr = []
        time_arr = []



app = webapp2.WSGIApplication([
    ('/', MainHandler)

], debug=True)
