import logging
import time
from slack_sdk.web import WebClient
from slack_sdk.webhook import WebhookClient
import os
from dotenv import load_dotenv
load_dotenv()

token= os.getenv('TOKEN')
client = WebClient(token)

response = client.chat_postMessage(channel="test-python-bot", text="Now it is 12:30. What do you want to eat for lunch?")
response = client.conversations_open(users=["U03LCF20JG2"])
print(response)

while(1):
    if (time.strftime('%H:%M', time.localtime()) == ("12:30")):
        response = client.chat_postMessage(channel="test-python-bot", text="Now it is 12:30. What do you want to eat for lunch?")
        time.sleep(60)