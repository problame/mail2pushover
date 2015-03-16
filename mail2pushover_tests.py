# -*- coding: utf-8 -*-

import unittest
from pushover_notification import PushoverNotification
import pushover_client, pushover_notification
from mail2pushover import Mail2Pushover
from email.header import Header, make_header


class TestPushoverClient(unittest.TestCase):

    def setUp(self):
        self.client = pushover_client.PushoverClient("usertoken", "apptoken")
    
    def test_empty_message_handling(self):
        note = PushoverNotification("a", "", "c")
        dict = self.client.post_fields_for_notification(note)
        
        self.assertDictEqual(dict, {"title":"a",
                                    "message" : "<No message>",
                                    "url":"c",
                                    "user":"usertoken",
                                    "token":"apptoken"})

    def test_post_fields(self):

        note = PushoverNotification("a", "b", "c")
        dict = self.client.post_fields_for_notification(note)

        self.assertDictEqual(dict, {  "title" : "a",
                                      "message" : "b",
                                      "url" : "c",
                                      "user" : "usertoken",
                                      "token" : "apptoken"
                                      })

class TestMail2Pushover(unittest.TestCase):

    def setUp(self):
        pass

    def test_notification_generation_mailinglist(self):

        fixture = open("fixtures/mailinglistmail.txt", "r")
        mail2p = Mail2Pushover(fixture)

        note = mail2p.generate_pushover_notification("message")

        self.assertEqual(note.title, "A list <list.example.com>")
        self.assertEqual(note.message, "Samplesubject")
        self.assertEqual(note.url, "message://%3C542248CE.9050202%40example.com%3E")

        fixture.close()

    def test_notification_generation_normalmail(self):

        fixture = open("fixtures/normalmail.txt", "r")
        mail2p = Mail2Pushover(fixture)

        note = mail2p.generate_pushover_notification("message")

        self.assertEqual(note.title, "Sender <sender@example.com>")
        self.assertEqual(note.message, u"Text with Umlaut ü")
        self.assertEqual(note.url, "message://%3C236899350.212129813731411556924226%40example.com%3E")

        fixture.close()


    def test_notification_generation_mail_with_special_char_in_sender(self):
        fixture = open("fixtures/mail_with_special_char_in_sender.txt", "r")
        mail2p = Mail2Pushover(fixture)

        note = mail2p.generate_pushover_notification("message")

    def test_invalid_headers(self):
        fixture = open("fixtures/mail_with_invalid_headers.txt", "r")
        mail2p = Mail2Pushover(fixture)

        note = mail2p.generate_pushover_notification("message")


    def test_notification_generation_mail_without_subject(self):
        fixture = open("fixtures/mailwithoutsubject.txt", "r")
        mail2p = Mail2Pushover(fixture)

        note = mail2p.generate_pushover_notification("message")

        self.assertEqual(note.message, "(No subject)")


    def test_custom_message_id_protocol(self):
        
        fixture = open("fixtures/normalmail.txt", "r")
        mail2p = Mail2Pushover(fixture)

        note = mail2p.generate_pushover_notification("customprotocol")
        
        self.assertEqual(note.url, "customprotocol://%3C236899350.212129813731411556924226%40example.com%3E")


if __name__ == '__main__':
    unittest.main()
