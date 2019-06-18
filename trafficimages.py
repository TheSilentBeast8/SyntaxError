import webapp2
from google.appengine.api import urlfetch
import json
import jinja2
import os

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        welcome_template = the_jinja_env.get_template('templates/index.html')
        #date_time = self.request.get("date")
        endpoint_url = "https://api.data.gov.sg/v1/transport/traffic-images"

        response = urlfetch.fetch(endpoint_url)
        content = response.content



        response_as_json = json.loads(content)

        print(response_as_json)






app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
