
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
url = os.getenv('URL_NGROK')
webhook = WebhookClient(url)
channel_name= os.getenv('CHANNEL_NAME')
channel_id= os.getenv('CHANNEL_ID')

def ReadRestaurantsFile():
    path = GetRestaurantsPath()
    return pd.read_csv(path)

def GetRestaurantsPath():
    try:
        db_path = os.getenv('FILE_LUNCH_PLACES')
        pd.read_csv(db_path)
        return db_path
    except:
        return 'ExampleLunchPlaces-info-Sheet1.csv'

def GetListPlaces(places_for_lunch_file):
    list_places = []
    for i in range(len(places_for_lunch_file)):
        for j in range(places_for_lunch_file.loc[i].at["Votes"]):
            list_places.append(places_for_lunch_file.loc[i].at["Name"])

    return list_places

def FormatHeaders(suggestion, places_for_lunch_file):
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

def FormatSuggestions(suggestion, places_for_lunch_file):
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

def getSuggestion(list_places, places_for_lunch_file, selection_num=3):
    suggestion_list = []
    real_selection_num = min(selection_num, len(places_for_lunch_file)) 

    while(len(suggestion_list) < real_selection_num):
        suggestion = list_places[randint(0, len(list_places) - 1)]
        if suggestion not in suggestion_list:
            suggestion_list.append(suggestion)

    return suggestion_list
    
def ChoseEmoji(suggestion, places_for_lunch_file):
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

    restaurants_file = ReadRestaurantsFile()
    list_places = GetListPlaces(restaurants_file)
    suggestions = getSuggestion(list_places, restaurants_file)
    emoji = ""
    num_emoji=0

    for sug in suggestions:
        num_emoji += 1
        blocks_2.append(FormatHeaders(sug, restaurants_file))
        blocks_2.append(FormatSuggestions(sug, restaurants_file))
        emoji += ChoseEmoji(sug, restaurants_file)+" = "+str(num_emoji)+"    "

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

    places_for_lunch_file = ReadRestaurantsFile()   

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
            file = GetRestaurantsPath(),
            channels = request.form["user_id"],
            title = "List restaurants suggestions"
        )
        return   """Check out your conversation with the bot to see the full "suggested restaurants" file"""
    else:
        places_for_lunch_file = ReadRestaurantsFile()
        return   "```\n" + str(places_for_lunch_file[["Name", "Emoji", "Votes", "Description", "Vegan", "Vegetarian"]]) + "\n```" + "\n" \
            "```\n" + str(places_for_lunch_file[["Delivery","Take-Away","Distance","Price range"]]) + "\n```" + "\n" \
            "```\n" + str(places_for_lunch_file[["Image"]]) + "\n```"

@app.route("/remove_row", methods=["POST"])
def CommandRemoveRowFile():
    db_path = GetRestaurantsPath()
    places_for_lunch_file = ReadRestaurantsFile()
    selected_row = int(request.form["text"])
    lines = []

    if selected_row > -1 and selected_row < len(places_for_lunch_file):
        with open(db_path, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()

        with open(db_path, 'w', encoding='utf-8') as fp:
            for number, line in enumerate(lines):
                if number != selected_row:
                    fp.write(line)

        return """Row {0} was removed from the "suggested restaurants" file""".format(selected_row)
    else:
        return "Wrong Input"

@app.route("/add_row", methods=["POST"])
def CommandAddRowFile():

    letter_pos = 0
    last_letter_pos = 0
    input_list = []
    freeze = False
    answer = request.form["text"]+","

    for i in answer:
        if i == '"' and freeze == False:
            freeze = True
        elif i == '"' and freeze == True:
            freeze = False
        elif i == "," and freeze == False:
            input_list += [request.form["text"][last_letter_pos:letter_pos]]
            last_letter_pos = letter_pos + 1
        letter_pos +=1

    if (len(input_list) == 11 and
        type(input_list[0]) == str and 
        input_list[1][0] == ":" and
        input_list[1][-1:] == ":" and
        input_list[2].isnumeric() == True and
        type(input_list[3]) == str and
        input_list[3][0] == '"' and
        input_list[3][-1:] == '"' and 
        (input_list[4] == ":seedling:" or input_list[4].isspace() == True) and
        (input_list[5] == ":carrot:" or input_list[5].isspace() == True) and
        (input_list[6] == "Delivery: :white_check_mark:" or input_list[6] == "Delivery: :x:") and
        (input_list[7] == "Take-Away: :white_check_mark:" or input_list[6] == "Take-Away: :x:") and
        ((input_list[8][:10] == 'Distance: ' and
        input_list[8][10].isnumeric() == True and
        input_list[8][-2:] == ' m') or 
        input_list[8] == "Distance: \\") and
        input_list[9][:13] == 'Price range: ' and
        input_list[9][13].isnumeric() == True and
        input_list[9][-1:] == "€" and 
        input_list[10][:8] == 'https://' and
        len(input_list[10]) > 8
        ):
    
        f = open(GetRestaurantsPath(), 'a', encoding='utf-8')
        f.write("\n"+request.form["text"])
        f.close()

        return """ "{0}"\n was added to the file containing the suggested restaurants""".format(request.form["text"])
    else:
        return "Element provided not in the right format. Try to watch the file containing the suggested restaurants as an example"