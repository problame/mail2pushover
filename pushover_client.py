import json
from pushover_notification import PushoverNotification
import httplib, urllib2, urllib

class PushoverClient:

    connection = None

    def __init__(self, user_token, app_token):
        self.user_token = user_token
        self.app_token = app_token
        self.connection = httplib.HTTPSConnection("api.pushover.net")

    def post_fields_for_notification(self, notification):
        assert isinstance(notification, PushoverNotification)
        return {    "title" : notification.title,
                    "message" : notification.message if len(notification.message) > 0 else "<No message>",
                    "url" : notification.url,
                    "token" : self.app_token,
                    "user" : self.user_token}

#http://stackoverflow.com/questions/6480723/urllib-urlencode-doesnt-like-unicode-values-how-about-this-workaround
    def encode_dict(self, map):
        return dict([(key,val.encode('utf-8')) for key, val in map.items() if isinstance(val, basestring)])

    def send_push_notification(self, notification):

        fields = self.post_fields_for_notification(notification)
        byteFields = self.encode_dict(fields)
        body = urllib.urlencode(byteFields)

        self.connection.connect()

        self.connection.request("POST", "/1/messages.json", body)
        response = self.connection.getresponse()
        self.connection.close()

        return response.status == 200

