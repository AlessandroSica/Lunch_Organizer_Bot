
import os
from random import randint
import pandas as pd
from flask import Flask

from slack_sdk.web import WebClient
from slack_sdk.webhook import WebhookClient

Token = os.getenv('TOKEN')
client = WebClient(Token)
App = Flask(__name__)

PlacesForLunchFile = pd.read_csv("LunchPlaces-info-Sheet9.csv")
ListPlaces = []
for i in range(len(PlacesForLunchFile)):

    for j in range(PlacesForLunchFile.loc[i].at["Votes"]):

        ListPlaces += [PlacesForLunchFile.loc[i].at["Name"]]

def FormatHeaders(Suggestion):

    for i in range(len(PlacesForLunchFile)):

        if Suggestion == PlacesForLunchFile.loc[i].at["Name"]:

            return {
			    "type": "header",
			    "text": {
			    	"type": "plain_text",
			    	"text": "{1} {0}".format(
                        PlacesForLunchFile.loc[i].at["Name"], 
                        PlacesForLunchFile.loc[i].at["Emoji"]
                    )
			    }
		    }

def FormatSuggestions(Suggestion):

    for i in range(len(PlacesForLunchFile)):

        if Suggestion == PlacesForLunchFile.loc[i].at["Name"]:

            return {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "{0}\n {1}{2}  -{3}​  -{4}​  -{5}\n {6}\n <{7}|Learn more...>\n"
                    .format(
                        PlacesForLunchFile.loc[i].at["Description"], 
                        PlacesForLunchFile.loc[i].at["Vegan "], 
                        PlacesForLunchFile.loc[i].at["Vegeterian"], 
                        PlacesForLunchFile.loc[i].at["Delivery"], 
                        PlacesForLunchFile.loc[i].at["Take-Away"], 
                        PlacesForLunchFile.loc[i].at["Distance"], 
                        PlacesForLunchFile.loc[i].at["Price range"], 
                        PlacesForLunchFile.loc[i].at["Tripadvisor"]
                    ),
                },
                "accessory": {
                    "type": "image",
                    "image_url": PlacesForLunchFile.loc[i].at["Image"],
                    "alt_text": "food image"
                }
            }

def getSuggestion():
    Suggestion = ListPlaces[randint(0, len(ListPlaces) - 1)]
    SuggestionList = [Suggestion]

    for i in range(2):
        NotDifferent = True

        while(NotDifferent):
            Suggestion = ListPlaces[randint(0, len(ListPlaces) - 1)]

            for j in (SuggestionList):

                if j == Suggestion:
                    Suggestion = SuggestionList[-1]
                    NotDifferent = True
                else:
                    NotDifferent = False

        SuggestionList += [Suggestion]

    return SuggestionList
    
def ChoseEmoji(Suggestion):

    for i in range(len(PlacesForLunchFile)):
        
        if Suggestion == PlacesForLunchFile.loc[i].at["Name"]:

            return PlacesForLunchFile.loc[i].at["Emoji"]

ChannelName= os.getenv('CHANNEL_NAME')
ThreadToken=0

@App.route('/')
def SendSuggestionLunch():
    global ThreadToken
    blocks1 = []
    blocks2 = []

    blocks1.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "Have you already decided where to lunch?"
        }
    })
    blocks1.append({
        "type": "section",
        "text": {
            "type": "plain_text", 
            "text": ":sunglasses: = Yes, I have already decided\n :dizzy_face: = No, what do you offer me?"
        }
    })
    blocks2.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "Here there are the suggestion of the day:"
        }
    })
    blocks2.append({"type": "divider"})

    Suggestions = getSuggestion()
    
    for suggestion in Suggestions:

        blocks2.append(FormatHeaders(suggestion))
        blocks2.append(FormatSuggestions(suggestion))
        
    Emoji1 = ChoseEmoji(Suggestions[0])
    Emoji2 = ChoseEmoji(Suggestions[1])
    Emoji3 = ChoseEmoji(Suggestions[2])

    blocks2.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Key*\n 🌱= vegan\n ​🥕​= vegetarian\n"
        }
    })
    blocks2.append({"type": "divider"})
    blocks2.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "Do you like any of them?\n React with the respective emoji"
        }
    })
    blocks2.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "{0} = 1,  {1} = 2,  {2} = 3".format(Emoji1, Emoji2, Emoji3)
        }
    })
    blocks2.append({"type": "divider"})

    response = client.chat_postMessage(channel = ChannelName, blocks = blocks1)
    ThreadToken = response["ts"]
    response = client.chat_postMessage(channel = ChannelName, thread_ts = ThreadToken, blocks = blocks2)

    return "GET"

@App.route('/Thread-Message')
def ThreadMessage():
    blocks3 = []

    blocks3.append({
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "This is a section block with checkboxes."
		},
		"accessory": {
			"type": "checkboxes",
			"options": [
				{
					"text": {
						"type": "mrkdwn",
						"text": "*this is mrkdwn text*"
					},
					"description": {
						"type": "mrkdwn",
						"text": "*this is mrkdwn text*"
					},
					"value": "value-0"
				},
				{
					"text": {
						"type": "mrkdwn",
						"text": "*this is mrkdwn text*"
					},
					"description": {
						"type": "mrkdwn",
						"text": "*this is mrkdwn text*"
					},
					"value": "value-1"
				},
				{
					"text": {
						"type": "mrkdwn",
						"text": "*this is mrkdwn text*"
					},
					"description": {
						"type": "mrkdwn",
						"text": "*this is mrkdwn text*"
					},
					"value": "value-2"
				}
			],
			"action_id": "checkboxes-action"
		}
	})

    response = client.chat_postMessage(channel = ChannelName, thread_ts = ThreadToken, blocks = blocks3)

    return "GET"