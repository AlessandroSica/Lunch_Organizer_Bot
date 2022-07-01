# Lunch_Organizer_Bot
## Organize your lunch with Lunch Bot <br>
This bot allow you to organize your lunch with your colleagues. It is coded in python and it is created to work on Slack. <br>
The bot sends you a message at a specific time on Slack, where it ask you if you have already decided where to lunch. <br>
Then it also gives you three suggestion on possible resturants to chose from, that are randomly chosen from a list. <br>
Then you can choose and see what the others chose by reacting to the message with the respective emoji of the restaurant. <br>

Example: <br>
![BotMessage](https://user-images.githubusercontent.com/85867861/176443233-96b2d252-500b-4d93-9874-ec7d24fc9c26.png)

## How to activate the bot:<br>

As a first step you need to create your slack app from this link: <br>
https://api.slack.com/apps <br>
And then generate your slack bot token form the page of slack regarding your app you just created. <br>

The next step is to install all the libraries required that are imported at the start of the program, you can do it using the terminal: <br>
`$ pip install pandas` <br>
`$ pip install flask` <br>
`$ pip install slack_sdk` <br>

Then you should create a the file contaning the suggestions on where to take the lunch. <br>
Use `ExampleLunchPlaces-info-Sheet1.csv` as a base for your file. <br>

After that you need to create a file (I chose .env and I made git ignore it) where you need to create a variable containing your bot token, 
one containing the channel ID of where you want to send the message, and the last one with the name of the file where there are the suggestions for the lunch. <br>
Example .env file: <br>
```
TOKEN=kygkgchgckyc-976597665858545fkykgckl-xbivku
CHANNEL_NAME=channel_name
FILE_LUNCH=file_name.csv
```

Then you can run this command in the folder of your project to start a local server: <br>
`python -m run flask` <br>

And then by refreshing the page of the local server on your browser, which will be named: <br>
`localhost:5000` <br>
(where the number after the colon is the port that is specified when you run the previous command) <br>
You will then get a message with three restaurant suggestions on the slack channel you specified! ;)
