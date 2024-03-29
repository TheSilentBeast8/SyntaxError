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

class MainHandler(webapp2.RequestHandler):
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
        print(len(response_as_json['area_metadata']))
        if len(response_as_json['area_metadata']) == 0:
            details = "The weather forecast only predicts for the next 24h! Please try again!"
            info = {'details':details
            }
        else:
            forecasts = response_as_json['items'][0]['forecasts']
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
    ('/', MainHandler)

], debug=True)
