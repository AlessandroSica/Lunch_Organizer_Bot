# Lunch_Organizer_Bot
## Organize your lunch with Lunch Bot <br>
This bot allow you to organize your lunch with your colleagues. It is coded in python and it is created to work on Slack. <br>
The bot sends you a message at a specific time on Slack, where it ask you if you have already decided where to lunch. <br>
Then it also gives you three suggestion on possible resturants to chose from, that are randomly chosen from a list. <br>
Then you can choose and see what the others chose by reacting to the message with the respective emoji of the restaurant. <br>

## Preview: <br>

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

## How to run your bot on Raspberry Pi and use a SSH to program it.

First thing you need to do is take your Raspberry pi and install on it an OS. <br>
See [the official documentation](https://www.raspberrypi.com/documentation/computers/getting-started.html) for more info. <br>
After you configure it you need to know its IP adress (check again the previous link). <br>
So after you pluged-in the Raspberry Pi, you attached it to the lan, or gave it access to the wifi network and if the device is near your computer, only then you can run the following code on your terminal, with the respectivee IP adress: <br>
example
`ssh pi@67.543.345.65` <br>
Then it will ask you to input a password, in this case the default one is `raspberry`, later it is suggested to change it for more security. <br>
After that you need to install python, making sure you install the right version of it: 3 or newer, you can do it by typing: <br>
`pip install python` <br>
(you check if you have the version 3 or newer by typing `python 3 --version`) <br>
And then you need to install also all the other libraries that you previously installed on your device, (look line 19). <br>
Now you can reach your folder by writing `cd` and then specifing the path to your folder: <br>
`cd Lunch_Organizer_Bot/` <br>
Then you can make a pull request from git in order to be sure that your file are updated by typing: <br>
`git pull` <br>
Now you should add your file with the list of the restaurants. So you can create a file by typing: <br>
`nano file_places.csv` <br>
This will open an enditor were you can paste what is inside the `file_places.csv` on your pc. <br>
Then you can close the editor and exit by pressing `CNTRL+C` and then `y` and `ENTER` to save the changes and go back. <br>
Now you should create your famous file `.env`, so you can type:
`nano .env` <br>
And in the editor you can paste what is inside the `.env` file on your pc. <br>
Then you can close the editor as we did before.
The next step is to create a file that will be run every time you plug in the Raspberry Pi and so you do a reboot. <br>
To do so you need to type, outside any folder (to return outside the folder just type `cd`):
`nano start-lunch-bot.sh` <br>
Use the name of the file you prefer but it needs to be a `.sh` file.
Then this will open the same text editor as before were you need to write: <br>
```
cd  ~/Lunch_Organizer_Bot/
python3 -m flask run`
```
(remember to write `python3` and not just `python`) <br>
Then you can close the editor.
Now, in order to make this file executable you need to type: <br>
`chmod +x start-lunch-bot.sh` <br>
Then you need to create three other files in the same way, one for each message. <br>
So in order to create the first one you need to type as we did before: <br>
`nano request.sh` <br>
Then in the editor you should write: <br>
`curl --location --request GET 'localhost:5000/'` <br>
In order to make a request to the server is specified in the code. <br>
Then you can close and save as we did before. <br>
Next, in oder to create the file for the second message you need to type: <br>
`nano request1.sh` <br>
And in the editor: <br>
`curl --location --request GET 'localhost:5000/Thread-Message'` <br>
Then you can close and save as we did before. <br>
And for the last message, try to guess... :
`nano request2.sh` <br>
And in the editor: <br>
`curl --location --request GET 'localhost:5000/Result-Voting'` <br>
After you have done this, remember that all this files need to be executable, as the one before so you need to type: <br>
`chmod +x request.sh` <br>
`chmod +x request1.sh` <br>
`chmod +x request2.sh` <br>
And now it is time to create your last, but probably most important file of all, the one that will tell to the Raspberry which file to execute at what time and when.<br>
In order to do so you need to type: <br>
`crontab -e` <br>
This will open another editor, where you need to write: <br>
```
@reboot ~/start-lunch-bot.sh
0 12 * * 0-5 ~/request.sh
30 12 * * 0-5 ~/request2.sh
10 13 * * 0-5 ~/request1.sh
```
Here you can write all the right names of your file, including the one that starts at every reboot and the other for three messages. <br> 
Then you can select the time you prefer by writing first the minutes and then the hour at which you want your bot to send the message. So in my case I decided to send my messages at `12:00`, `12:30` and `13:10`. And then you can select also which day of the week the bot should send the message. I chose from monday to friday, so `0-5`. For more info on how to specify when to send the message this is what the values should be in order (as it is said in the editor): <br>
1. m - Minute - 0 through 59
2. h - Hour - 0 through 23
3. dom - Day of Month - 0 through 31
4. mon - Month - 0 through 12
5. dow - Day of Week - 0 through 7 (0 and 7 are both Sunday)
(asterisk means always) <br>
Then you can close the editor. <br>
And if you want you can do a reboot by typing: <br>
`sudo reboot` <br>
After that your Raspberry Pi should be ready to go! When you want to use it you just need to plug it in.
And if you want connect again to it just type the first command we typed before to connect: <br>
`ssh pi@67.543.345.65` <br>
Just remember to use the right IP adress.
