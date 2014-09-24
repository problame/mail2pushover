class PushoverNotification:
    message = ""
    title = ""
    url = ""
    def __init__(self, title, message, url):
        self.title = title
        self.message = message
        self.url = url
