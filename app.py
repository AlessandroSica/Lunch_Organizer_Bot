import pandas as pd
from random import randint
from flask import Flask
import logging
import time
from slack_sdk.web import WebClient
from slack_sdk.webhook import WebhookClient
import os
from dotenv import load_dotenv
load_dotenv()

token= os.getenv('TOKEN')
client = WebClient(token)
app = Flask(__name__)

@app.route('/', methods=["POST"])
def POST():
    print("post")
    return "POST"

@app.route('/', methods=["PUT"])
def PUT():
    return "PUT"

@app.route('/', methods=["DELETE"])
def DELETE():
    return "DELETE"

PlacesForLunchFile= pd.read_csv("PlacesLunch-Sheet1.csv")
#print(PlacesForLunchFile)
ListPlaces=[]
for i in range(len(PlacesForLunchFile)):
    for j in range(PlacesForLunchFile.loc[i].at["Votes"]):
        ListPlaces+=[PlacesForLunchFile.loc[i].at["Name"]]
#print(ListPlaces)
@app.route('/')
def SendMessage():
    if (time.strftime('%H:%M', time.localtime()) == ("11:30")):
        response = client.chat_postMessage(channel="office", text="*Have you already decided where to lunch? (🙂 = Yes, 😐 = No)*")
        response = client.chat_postMessage(channel="office", 
        blocks=[{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Here there are the suggestion of the day:*"
			}
		},
        {
			"type": "divider"
		}])
        for i in range(3):
            response = client.chat_postMessage(channel="office", text=(ListPlaces[randint(0, len(ListPlaces)-1)]), link_names="", icon_emoji="", )
    return "GET"

@app.route('/tests/:id')
def test():
    return "GET a new test"