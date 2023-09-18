#!/usr/bin/python3

from exchangelib import Configuration, Credentials, Message, Mailbox, Account, DELEGATE
import os

USERNAME = os.getenv('EMAIL_USERNAME')
PASSWORD = os.getenv('EMAIL_PASSWORD')

credentials = Credentials(username = USERNAME, password = PASSWORD)

config = Configuration(server="outlook.office365.com", credentials=credentials)

account = Account(
    primary_smtp_address = USERNAME,
    config=config,
    autodiscover=False,
    access_type=DELEGATE,
)


m = Message(
    account=account,
    subject="Test",
    body="Test",
    to_recipients=[
        Mailbox(email_address=USERNAME),
    ],
    # Simple strings work, too
    cc_recipients=[USERNAME],
)
m.send()