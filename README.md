A small python script that takes e-mails from *stdin* or a file, reads some headers and sends push notifications to mobile devices using the [Pushover](https://pushover.net).


In addition to *subject* and *sender*, the push notifications contain a URL in the following format: `message://\<Message-ID header value\>`

On iOS, the `message://` URL scheme is assigned to *MobileMail.app*. The app will open when tapping on the URL and if the mail is in the inbox, it will be opened.

Unfortunately, there is no way to make *MobileMail.app* open messages that are not in the inbox. If you prefer another mail client that has a URL scheme, change it using the config flag explained below.

#Configuration

Some values have to be set in `config.json`.

* `user_key`: Your Pushover user API key
* `app_token`: Your Pushover app token
* `message_id_protocol`: If you want another URL scheme, e.g. to open a third-party mail client, you can replace `message` with your desired protocol, e.g. `x-dispatch` for [Dispatch.app](http://www.dispatchapp.net/faq.html#openDispatchLinksOnMac)

#Usage

The script is writting for Python 2.7 and designed to be called from `qmail` or some other MTA. The original usecase was a hook into a `.qmail` script on [uberspace](https://wiki.uberspace.de/mail:dotqmail) script.

##Configuration

Copy the `config.json.example` to `config.json` and change the permissions to hide your Pushover keys from other users using `chmod 640 config.json`.

##Test configuration

For debugging purposes, you might want to run `mail2pushover` from the command line before adding it to your .qmail file. Some fixtures are inlcuded in the repository.

	/usr/local/bin/python2.7 mail2pushover.py --config /path/to/config.json --mailfile fixtures/normalmail.txt


##Include in .qmail file

To actually receive push notifications when new mail arrives, add the following line to your `.qmail-<username>` file

	/usr/local/bin/python2.7 /path/to/mail2pushover.py --config /path/to/config.json

