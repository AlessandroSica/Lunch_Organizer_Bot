
import os
from random import randint
import pandas as pd
from flask import Flask

from slack_sdk.web import WebClient
from slack_sdk.webhook import WebhookClient

token = os.getenv('TOKEN')
client = WebClient(token)
app = Flask(__name__)

places_for_lunch_file = pd.read_csv(os.getenv('FILE_LUNCH'))
list_places = []
for i in range(len(places_for_lunch_file)):

    for j in range(places_for_lunch_file.loc[i].at["Votes"]):

        list_places += [places_for_lunch_file.loc[i].at["Name"]]

def FormatHeaders(suggestion):

    for i in range(len(places_for_lunch_file)):

        if suggestion == places_for_lunch_file.loc[i].at["Name"]:

            return {
			    "type": "header",
			    "text": {
			    	"type": "plain_text",
			    	"text": "{1} {0}".format(
                        places_for_lunch_file.loc[i].at["Name"], 
                        places_for_lunch_file.loc[i].at["Emoji"]
                    )
			    }
		    }

def FormatSuggestions(suggestion):

    for i in range(len(places_for_lunch_file)):

        if suggestion == places_for_lunch_file.loc[i].at["Name"]:

            return {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "{0}\n {1}{2}  -{3}​  -{4}​  -{5}\n {6}\n <{7}|Learn more...>\n"
                    .format(
                        places_for_lunch_file.loc[i].at["Description"], 
                        places_for_lunch_file.loc[i].at["Vegan "], 
                        places_for_lunch_file.loc[i].at["Vegeterian"], 
                        places_for_lunch_file.loc[i].at["Delivery"], 
                        places_for_lunch_file.loc[i].at["Take-Away"], 
                        places_for_lunch_file.loc[i].at["Distance"], 
                        places_for_lunch_file.loc[i].at["Price range"], 
                        places_for_lunch_file.loc[i].at["Tripadvisor"]
                    ),
                },
                "accessory": {
                    "type": "image",
                    "image_url": places_for_lunch_file.loc[i].at["Image"],
                    "alt_text": "food image"
                }
            }

def getSuggestion():
    suggestion = list_places[randint(0, len(list_places) - 1)]
    suggestion_list = [suggestion]

    for i in range(2):
        NotDifferent = True

        while(NotDifferent):
            suggestion = list_places[randint(0, len(list_places) - 1)]

            for j in (suggestion_list):

                if j == suggestion:
                    suggestion = suggestion_list[-1]
                    NotDifferent = True
                else:
                    NotDifferent = False

        suggestion_list += [suggestion]

    return suggestion_list
    
def ChoseEmoji(suggestion):

    for i in range(len(places_for_lunch_file)):
        
        if suggestion == places_for_lunch_file.loc[i].at["Name"]:

            return places_for_lunch_file.loc[i].at["Emoji"]

channel_name= os.getenv('CHANNEL_NAME')

@app.route('/')
def SendSuggestionLunch():
    global thread_token
    blocks_1 = []
    blocks_2 = []

    blocks_1.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "Have you already decided where to lunch?"
        }
    })
    blocks_1.append({
        "type": "section",
        "text": {
            "type": "plain_text", 
            "text": ":sunglasses: = Yes, I have already decided\n :dizzy_face: = No, what do you offer me?"
        }
    })
    blocks_2.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "Here there are the suggestion of the day:"
        }
    })
    blocks_2.append({"type": "divider"})

    suggestions = getSuggestion()
    
    for sug in suggestions:

        blocks_2.append(FormatHeaders(sug))
        blocks_2.append(FormatSuggestions(sug))
        
    emoji1 = ChoseEmoji(suggestions[0])
    emoji2 = ChoseEmoji(suggestions[1])
    emoji3 = ChoseEmoji(suggestions[2])

    blocks_2.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Key*\n 🌱= vegan\n ​🥕​= vegetarian\n"
        }
    })
    blocks_2.append({"type": "divider"})
    blocks_2.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "Do you like any of them?\n React with the respective emoji"
        }
    })
    blocks_2.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "{0} = 1,  {1} = 2,  {2} = 3".format(emoji1, emoji2, emoji3)
        }
    })
    blocks_2.append({"type": "divider"})

    response = client.chat_postMessage(channel = channel_name, blocks = blocks_1)
    thread_token = response["ts"]
    response = client.chat_postMessage(channel = channel_name, thread_ts = thread_token, blocks = blocks_2)

    return "GET"

@app.route('/Thread-Message')
def ThreadMessage():
    blocks_3 = []

    blocks_3.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "Almost lunch time! Choose your place and go to grab food!"
        }
    })

    blocks_3.append({
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "If you are staying in the office, where do you want to lunch?\n \
            :one: rooftop\n \
            :two: lounge terrace\n \
            :three: lounge\n \
            :four: office 411 terrace\n \
            :five: kitchen area 3 floor\n \
            :six: relax area 2 floor"
		}
    })

    response = client.chat_postMessage(channel = channel_name, thread_ts = thread_token, blocks = blocks_3)
    result = client.conversations_history(
        channel="C03M32EE1K2",
        inclusive=True,
        oldest=thread_token,
        limit=1
    )
    print(result)
    print(result['latest_reply'])
    return "GET"