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

PlacesForLunchFile= pd.read_csv("LunchPlaces-info-Sheet1(1).csv")
ListPlaces=[]
for i in range(len(PlacesForLunchFile)):
    for j in range(PlacesForLunchFile.loc[i].at["Votes"]):
        ListPlaces+=[PlacesForLunchFile.loc[i].at["Name"]]

def FormatHeaders(Suggestion):
    for i in range(len(PlacesForLunchFile)):
        if Suggestion==PlacesForLunchFile.loc[i].at["Name"]:
            return {
			    "type": "header",
			    "text": {
			    	"type": "plain_text",
			    	"text": PlacesForLunchFile.loc[i].at["Name"]
			    }
		    }

def FormatSuggestions(Suggestion):
    for i in range(len(PlacesForLunchFile)):
        if Suggestion==PlacesForLunchFile.loc[i].at["Name"]:
            return {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*{0}* ​{1}​ {2}\n {3}\n {4}{5}\n {6}​\n {7}​\n {8}\n {9}\n <{10}| Learn more...>\n".format(PlacesForLunchFile.loc[i].at["Rating"], PlacesForLunchFile.loc[i].at["Stars"], PlacesForLunchFile.loc[i].at["Reviews"], PlacesForLunchFile.loc[i].at["Description"], PlacesForLunchFile.loc[i].at["Vegan "], PlacesForLunchFile.loc[i].at["Vegeterian"], PlacesForLunchFile.loc[i].at["Delivery"], PlacesForLunchFile.loc[i].at["Take-Away"], PlacesForLunchFile.loc[i].at["Distance"], PlacesForLunchFile.loc[i].at["Price range"], PlacesForLunchFile.loc[i].at["Tripadvisor"])
                },
                "accessory": {
                    "type": "image",
                    "image_url": PlacesForLunchFile.loc[i].at["Image"],
                    "alt_text": "food image"
                }
            }

def getSuggestion():
    Suggestion=ListPlaces[randint(0, len(ListPlaces)-1)]
    SuggestionList=[Suggestion]
    for i in range(2):
        NotDifferent=True
        while(NotDifferent):
            Suggestion=ListPlaces[randint(0, len(ListPlaces)-1)]
            for j in (SuggestionList):
                if j==Suggestion:
                    Suggestion=SuggestionList[-1]
                    NotDifferent=True
                else:
                    NotDifferent=False
        SuggestionList+=[Suggestion]
    return SuggestionList

@app.route('/')
def SendSuggestionLunch():
    blocks=[]

    blocks.append({"type": "header","text": {"type": "plain_text", "text": "Have you already decided where to lunch? (🙂 = Yes, 😐 = No)\n Here there are the suggestion of the day:"}})
    blocks.append({"type": "divider"})

    Suggestions=getSuggestion()
    
    for suggestion in Suggestions:
        blocks.append(FormatHeaders(suggestion))
        blocks.append(FormatSuggestions(suggestion))

    blocks.append({"type": "divider"})
    blocks.append({"type": "section","text": {"type": "mrkdwn","text": "*Key*\n 🌱= vegan\n ​🥕​= vegetarian\n "}})
    blocks.append({"type": "divider"})
    
    response = client.chat_postMessage(channel="test-python-bot", blocks=blocks)
    
    return "GET"

@app.route('/tests/:id')
def test():
    return "GET a new test"