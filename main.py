import webapp2
from google.appengine.api import urlfetch
import json
import jinja2
import os
import urllib

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Welcome(webapp2.RequestHandler):
    def get(self):
        main_template = the_jinja_env.get_template('templates/homepage.html')
        self.response.write(main_template.render())

class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_template = the_jinja_env.get_template('templates/website.html')
        self.response.write(main_template.render())

class SocialMedia(webapp2.RequestHandler):
    def get(self):
        main_template = the_jinja_env.get_template('templates/socialmedia.html')
        self.response.write(main_template.render())

class Traffic(webapp2.RequestHandler):
    def get(self):
        welcome_template = the_jinja_env.get_template('templates/index.html')
        self.response.write(welcome_template.render())


class WeatherHandler(webapp2.RequestHandler):
    def get(self):
        welcome_template = the_jinja_env.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())


    def post(self):
        welcome_template = the_jinja_env.get_template('templates/welcome.html')
        date = self.request.get("date")
        time = self.request.get("time")
        time_change = urllib.quote(time, safe='')
        datetime = date+'T'+time_change+'%3A00'
        location = self.request.get("location")
        print(location)
        print(time)
        print(date)

        endpointUrl = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast?date_time="+datetime
        #print(endpointUrl)

        response = urlfetch.fetch(endpointUrl)

        content = response.content

        response_as_json = json.loads(content)
        forecasts = response_as_json['items'][0]['forecasts']
        #print(forecasts)
        forecast = ''
        for data in forecasts:
            if data['area'] == location:
                forecast = data['forecast']
                break

        info = {
            "forecast":"Forecast at "+location+' on '+date+' '+time+' shows '+ forecast +' weather',
            "location": location,
            "time": time,
            "date": date,
        }
        self.response.write(welcome_template.render(info))




app = webapp2.WSGIApplication([
    ('/', Welcome),
    ('/welcome', MainHandler),
    ('/weather', WeatherHandler),
    ('/sm', SocialMedia),
    ('/traffic', Traffic),
], debug=True)
