from exchangelib import Credentials, Account
import os

USERNAME = os.getenv('EMAIL_USERNAME')
PASSWORD = os.getenv('EMAIL_PASSWORD')
print(USERNAME)
print(PASSWORD)

credentials = Credentials(USERNAME, PASSWORD)
account = Account(USERNAME, credentials=credentials, autodiscover=True)

for item in account.inbox.all().order_by("-datetime_received")[:100]:
    print(item.subject, item.sender, item.datetime_received)