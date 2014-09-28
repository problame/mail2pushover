from email.parser import Parser, Message
from email.header import Header, decode_header
import sys
import argparse
from pushover_notification import PushoverNotification
from pushover_client import PushoverClient
import urllib
import json

from sys import stdin

class Mail2Pushover:

    def __init__(self, file):
        self.message = Parser().parse(file, headersonly=True)

    def get_mail_header_value(self, header):
        assert isinstance(header, str)

        unicodeValue = u' '.join(w.decode(e or 'ascii') for w,e in decode_header(header))

        return unicodeValue


    def generate_pushover_notification(self, url_protocol):
        assert isinstance(self.message, Message)

        isListMail = self.message["List-ID"] != None
        title = ""
        if isListMail:
            title = self.get_mail_header_value(self.message["List-ID"])
        else:
            title = self.get_mail_header_value(self.message["From"])

        body = self.get_mail_header_value(self.message["Subject"])
        url = u"%s://%s" % (url_protocol, urllib.quote(self.get_mail_header_value(self.message["Message-ID"])))

        note = PushoverNotification(title, body, url)

        return note




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Options parser.')
    parser.add_argument("--config", metavar="config_file", type=file, nargs=1, help="Path to a file like config.json.example")
    parser.add_argument("--mailfile", metavar="mail_file", type=file, nargs=1, help='Path to a file which contains a mail')
    parser.add_argument("--title", metavar="custom_title", type=unicode, nargs=1, help="A custom title to use instead of the one inferred from the e-mail.")
    args = parser.parse_args()

    config = json.load(args.config[0])

    pushover = PushoverClient(config["user_key"], config["app_token"])

    file = args.mailfile[0] if args.mailfile else sys.stdin

    m2p = Mail2Pushover(file)

    note = m2p.generate_pushover_notification(config["message_id_protocol"])

    if args.title:
        note.title = args.title[0]

    success = pushover.send_push_notification(note)

    sys.exit(0 if success else 1)