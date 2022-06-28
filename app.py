import pandas as pd
from random import randint
from flask import Flask
import logging
import time
from slack_sdk.web import WebClient
from slack_sdk.webhook import WebhookClient
import os

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

PlacesForLunchFile= pd.read_csv("LunchPlaces-info-Sheet8.csv")
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
                    "text": "{0}\n {1}{2}  -{3}​  -{4}​  -{5}\n {6}\n <{7}|Learn more...>\n".format(PlacesForLunchFile.loc[i].at["Description"], PlacesForLunchFile.loc[i].at["Vegan "], PlacesForLunchFile.loc[i].at["Vegeterian"], PlacesForLunchFile.loc[i].at["Delivery"], PlacesForLunchFile.loc[i].at["Take-Away"], PlacesForLunchFile.loc[i].at["Distance"], PlacesForLunchFile.loc[i].at["Price range"], PlacesForLunchFile.loc[i].at["Tripadvisor"]),
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
    
def ChoseEmoji(Suggestion):
    for i in range(len(PlacesForLunchFile)):
        if Suggestion==PlacesForLunchFile.loc[i].at["Name"]:
            return PlacesForLunchFile.loc[i].at["emoji"]

ChannelName= os.getenv('CHANNEL_NAME')

@app.route('/')
def SendSuggestionLunch():
    global ThreadToken
    blocks1=[]
    blocks2=[]

    blocks1.append({"type": "header","text": {"type": "plain_text", "text": "Have you already decided where to lunch?"}})
    blocks1.append({"type": "header","text": {"type": "plain_text", "text": ":sunglasses: = Yes, I have already decided\n :dizzy_face: = No, I don't know what to do"}})
    blocks2.append({"type": "header","text": {"type": "plain_text", "text": "Here there are the suggestion of the day:"}})
    blocks2.append({"type": "divider"})

    Suggestions=getSuggestion()
    
    for suggestion in Suggestions:
        blocks2.append(FormatHeaders(suggestion))
        blocks2.append(FormatSuggestions(suggestion))
    emoji1=ChoseEmoji(Suggestions[0])
    emoji2=ChoseEmoji(Suggestions[1])
    emoji3=ChoseEmoji(Suggestions[2])

    blocks2.append({"type": "section","text": {"type": "mrkdwn","text": "*Key*\n 🌱= vegan\n ​🥕​= vegetarian\n "}})
    blocks2.append({"type": "divider"})
    blocks2.append({"type": "header","text": {"type": "plain_text", "text": "Do you like any of them?\n {0} = 1\n {1} = 2\n {2} = 3".format(emoji1, emoji2, emoji3)}})
    blocks2.append({"type": "divider"})

    response = client.chat_postMessage(channel=ChannelName, blocks=blocks1)
    ThreadToken=response["ts"]
    response = client.chat_postMessage(channel=ChannelName, thread_ts=ThreadToken, blocks=blocks2)

    return "GET"

@app.route('/Thread Message')
def ThreadMessage():
    response = client.chat_postMessage(channel=ChannelName, thread_ts=ThreadToken, text="Have you decided now? Hurry up!")

    return "GET"