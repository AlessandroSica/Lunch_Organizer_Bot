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
#@app.route('/')
#def indexGET():
#    return "GET"

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

@app.route('/')
def SendMessage():
    if (time.strftime('%H:%M', time.localtime()) == ("12:00")):
        response = client.chat_postMessage(channel="office", text="Avete già ordinato il pranzo? (🙂 = si, 😐 = no)")
        time.sleep(60)
    return "GET"

@app.route('/tests/:id')
def test():
    return "GET a new test"