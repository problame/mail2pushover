from email.parser import Parser, Message
from email.header import Header, decode_header
import sys
import argparse
from pushover_notification import PushoverNotification
from pushover_client import PushoverClient
import urllib
import json
import re

from sys import stdin

class Mail2Pushover:

    def __init__(self, file):
        self.message = Parser().parse(file, headersonly=True)

    def get_mail_header_value(self, header):
        assert isinstance(header, str)

        unicodeValue = u' '.join(w.decode(e or 'ascii') for w,e in decode_header(header))

        return unicodeValue


    def generate_pushover_notification(self, url_protocol, short_auto_title=False):
        assert isinstance(self.message, Message)

        isListMail = self.message["List-ID"] != None
        title = ""
        if isListMail:
            title = self.get_mail_header_value(self.message["List-ID"])
        else:
            title = self.get_mail_header_value(self.message["From"])


        if short_auto_title:
            name_match = re.search(r"^(.+\S)\s*<", title)
            if name_match and len(name_match.groups()) > 0:
                title = name_match.group(1)
            else:
                mail_match = re.search(r"([a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)", title, re.IGNORECASE)
                if mail_match and len(mail_match.groups()) > 0:
                    title = mail_match.group(1)


        #Subject is optional according to http://tools.ietf.org/html/rfc2822#section-3.6
        subject_header = self.message["Subject"]
        body = self.get_mail_header_value(subject_header) if isinstance(subject_header, str) else "(No subject)"


        #Subject should be present but is not required according to http://tools.ietf.org/html/rfc2822#section-3.6
        message_id_header = self.message["Message-ID"]
        if message_id_header:
            url = u"%s://%s" % (url_protocol, urllib.quote(self.get_mail_header_value(message_id_header)))

        note = PushoverNotification(title, body, url)

        return note




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Options parser.')
    parser.add_argument("--config", metavar="config_file", type=file, nargs=1, help="Path to a file like config.json.example")
    parser.add_argument("--mailfile", metavar="mail_file", type=file, nargs=1, help='Path to a file which contains a mail')
    parser.add_argument("--title", metavar="custom_title", type=unicode, nargs=1, help="A custom title to use instead of the one inferred from the e-mail.")
    parser.add_argument("--short-auto-title", type=bool, help="Set this flag to infer shorter titles for the notifications. E.g. 'Sender <sender@example.com>' would be 'Sender' only.")
    args = parser.parse_args()

    config = json.load(args.config[0])

    pushover = PushoverClient(config["user_key"], config["app_token"])

    file = args.mailfile[0] if args.mailfile else sys.stdin

    m2p = Mail2Pushover(file)

    note = m2p.generate_pushover_notification(config["message_id_protocol"], short_auto_title=args.short_auto_title)

    if args.title:
        note.title = args.title[0]

    success = pushover.send_push_notification(note)

    sys.exit(0 if success else 1)