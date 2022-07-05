
import os
from random import randint
from secrets import randbelow
from this import d
import pandas as pd
from flask import Flask, request

from slack_sdk.web import WebClient
from slack_sdk.webhook import WebhookClient

token = os.getenv('TOKEN')
client = WebClient(token)
app = Flask(__name__)
db_path = os.getenv('FILE_LUNCH')
url = os.getenv('URL_NGROK')
webhook = WebhookClient(url)
channel_name= os.getenv('CHANNEL_NAME')
channel_id= os.getenv('CHANNEL_ID')

try:
    places_for_lunch_file = pd.read_csv(db_path)
except:
    db_path = 'ExampleLunchPlaces-info-Sheet1.csv'
    places_for_lunch_file = pd.read_csv(db_path)

list_places = []
for i in range(len(places_for_lunch_file)):
    for j in range(places_for_lunch_file.loc[i].at["Votes"]):
        list_places.append(places_for_lunch_file.loc[i].at["Name"])

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
                    "text": "{0}\n {1}{2}\n  -{3}​  -{4}​  -{5}\n {6}" #`{7}`
                    .format(
                        places_for_lunch_file.loc[i].at["Description"], 
                        places_for_lunch_file.loc[i].at["Vegan"], 
                        places_for_lunch_file.loc[i].at["Vegetarian"], 
                        places_for_lunch_file.loc[i].at["Delivery"], 
                        places_for_lunch_file.loc[i].at["Take-Away"], 
                        places_for_lunch_file.loc[i].at["Distance"], 
                        places_for_lunch_file.loc[i].at["Price range"], #places_for_lunch_file.loc[i].at["Tripadvisor"]
                    ),
                },
                "accessory": {
                    "type": "image",
                    "image_url": places_for_lunch_file.loc[i].at["Image"],
                    "alt_text": "food image"
                }
            }

def getSuggestion(selection_num=3):
    suggestion_list = []
    real_selection_num = min(selection_num, len(places_for_lunch_file)) 

    while(len(suggestion_list) < real_selection_num):
        suggestion = list_places[randint(0, len(list_places) - 1)]
        if suggestion not in suggestion_list:
            suggestion_list.append(suggestion)

    return suggestion_list
    
def ChoseEmoji(suggestion):
    for i in range(len(places_for_lunch_file)):
        if suggestion == places_for_lunch_file.loc[i].at["Name"]:
            return places_for_lunch_file.loc[i].at["Emoji"]

@app.route('/')
def SendSuggestionLunch():
    global thread_token
    blocks_1 = []
    blocks_2 = []

    blocks_1.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "Are you already set for lunch?"
        }
    })
    blocks_1.append({
        "type": "section",
        "text": {
            "type": "plain_text", 
            "text": ":gatto-sunglasses: = Yes, I am fine\n :moschi: = No, what do you offer me?"
        }
    })
    blocks_2.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "Here there are the suggestions of the day:"
        }
    })
    blocks_2.append({"type": "divider"})

    suggestions = getSuggestion()
    emoji = ""
    num_emoji=0

    for sug in suggestions:
        num_emoji += 1
        blocks_2.append(FormatHeaders(sug))
        blocks_2.append(FormatSuggestions(sug))
        emoji += ChoseEmoji(sug)+" = "+str(num_emoji)+"    "

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
            "text": "Do you like any of them?\n React with the respective emoji of any reastaurant you want"
        }
    })
    blocks_2.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "{0}\n :stuck_out_tongue_winking_eye: = for me is the same!".format(emoji)
        }
    })
    blocks_2.append({"type": "divider"})

    response = client.chat_postMessage(channel = channel_name, blocks = blocks_1)
    thread_token = response["ts"]
    response = client.chat_postMessage(channel = channel_name, thread_ts = thread_token, blocks = blocks_2)

    return "GET"

@app.route('/Place-Message')
def PlaceMessage():
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

    response = client.chat_postMessage(channel = channel_name, blocks = blocks_3)

    return "GET"

@app.route('/Result-Voting')
def ResultVoteMessage():
    blocks_4 = []

    blocks_4.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "It is time to order your lunch!"
        }
    })

    result = client.conversations_replies(
        channel = channel_id,
        inclusive = True,
        ts = thread_token,
        oldest = thread_token,
        limit = 1
    )

    try: 
        result['messages'][1]['reactions']
    except:
        response = client.chat_postMessage(channel = channel_name, thread_ts = thread_token, blocks = blocks_4)
        return "GET"

    list_emoji = []

    for i in places_for_lunch_file["Emoji"]:
        list_emoji += [i]

    list_answer = []

    for i in range(len(result['messages'][1]['reactions'])):
        if ":"+result['messages'][1]['reactions'][i]['name']+":" in list_emoji:
            list_answer += [(result['messages'][1]['reactions'][i]['name'], result['messages'][1]['reactions'][i]['count'])]

    if list_answer == []:
        return "GET"

    highest_vote = 0
    winners_emoji = []

    for i in list_answer:
        (place, vote) = i
        if vote > highest_vote:
            highest_vote = vote
            winners_emoji = [place]
        elif vote == highest_vote:
            winners_emoji += [place]

    winners_places = ""

    for i in winners_emoji:
        for j in range(len(places_for_lunch_file["Emoji"])):
            if ":"+i+":" == places_for_lunch_file.loc[j].at["Emoji"]:
                winners_places += "- "+places_for_lunch_file.loc[j].at["Name"]+"\n"

    blocks_4.append({
        "type": "header",
        "text": {
            "type": "plain_text", 
            "text": "We have a winner, the most voted restaurant is:\n {0}".format(winners_places)
        }
    })

    response = client.chat_postMessage(channel = channel_name, thread_ts = thread_token, blocks = blocks_4)

    return "GET"

@app.route("/list_lunch_places", methods=["POST"])
def CommandShowFile():
    if request.form["text"] == "raw":
        response = client.files_upload(
            file = db_path,
            channels = request.form["user_id"],
            title = "List restaurants suggestions"
        )
        return   """Check out your conversation with the bot to see the full "suggested restaurants" file"""
    else:
        return   "```\n" + str(places_for_lunch_file[["Name", "Emoji", "Votes", "Description", "Vegan", "Vegetarian"]]) + "\n```" + "\n" \
            "```\n" + str(places_for_lunch_file[["Delivery","Take-Away","Distance","Price range","Image"]]) + "\n```"

@app.route("/remove_row", methods=["POST"])
def CommandRemoveRowFile():
    global places_for_lunch_file, db_path

    selected_row = int(request.form["text"])
    lines = []

    if selected_row > -1 and selected_row <= len(places_for_lunch_file):
        with open(db_path, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()

        with open(db_path, 'w', encoding='utf-8') as fp:
            for number, line in enumerate(lines):
                if number != selected_row:
                    fp.write(line)

        try:
            places_for_lunch_file = pd.read_csv(db_path)
        except:
            db_path = 'ExampleLunchPlaces-info-Sheet1.csv'
            places_for_lunch_file = pd.read_csv(db_path)

        return """Row {0} was removed from the "suggested restaurants" file""".format(selected_row)
    else:
        return "Wrong Input"