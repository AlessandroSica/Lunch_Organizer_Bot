# Lunch_Organizer_Bot
## Organize your lunch with Lunch Bot <br>
This bot allows you to organize your lunch with your colleagues. It is coded in python and it is created to work on Slack. <br>
The bot sends you a message at a specific time on Slack, where it asks you if you have already decided where to lunch. <br>
Then it also gives you three suggestions on possible restaurants to chose from, that are randomly chosen from a list. <br>
Then you can choose and see what the others chose by reacting to the message with the respective emoji of the restaurant. <br>
After that the bot with another messageto will remind you to order your lunch, and it will also say which was the restaurant with the most reactions. <br>
Then it will send a final message where it suggests you to go and grab food, and ask you where you would like to lunch. You can answer by reacting with the respective number of the place you want, which you can choose between the list of option shown. <br>
There are also slash commands that can be used to see the file containing the restaurants suggestion, to add a new row to it or to remove an already existing one. <br>

## Preview: <br>
channel: <br>
![image](https://user-images.githubusercontent.com/85867861/177526138-c0db6196-2760-45c6-94fa-c237f7dfb0ef.png)
##
tread:  <br>
![image](https://user-images.githubusercontent.com/85867861/177178620-c37ad306-7062-496e-a480-dbbc6ec7a6bb.png)
![![MessageBot](https://user-images.githubusercontent.com/85867861/177526754-c4935a43-2af6-4427-a90e-5de28e8922a8.png)

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
CHANNEL_ID=G5UDHEJSB4
FILE_LUNCH=file_name.csv
```

Then you can run this command in the folder of your project to start a local server: <br>
`python -m run flask` <br>

And then by refreshing the page of the local server on your browser, which will be named: <br>
`localhost:5000` <br>
(where the number after the colon is the port that is specified when you run the previous command) <br>
You will then get a message, in the channel you specified, that ask you if you are already set for lunch or not, and here you can answer with two emoji to say if you are fine or not. <br>
![image](https://user-images.githubusercontent.com/85867861/177570151-dc474777-58df-4392-903a-70613230194f.png)
<br>
<br>
Then with the same message in the thread you will get three restaurant suggestions which you can vote for by reacting with the respective emoji of the restaurants suggested or of any restaurant present in your file containig all the restaurants info. <br>
![image](https://user-images.githubusercontent.com/85867861/177570309-13339ad0-07ae-40af-bda8-754257c6a26f.png)
<br>
<br>
Instead refresh the page: <br>
`localhost:5000/Result-Voting` <br>
You will get a second message in the thread of the message before that will remeber you to order your lunch and it will also tell you which was the restaurant with the most reactions. <br>
![image](https://user-images.githubusercontent.com/85867861/177568321-7453afc9-6154-4594-8d8b-862ab9d247ff.png)
<br>
<br>
And if you refresh the page: <br>
`localhost:5000/Place-Message` <br>
Yuo will receive the last message, in the cahannel this time, where the bot will tell you to go and grab food and it will also ask you where do you want to lunch. You can answer by reacting with the respective number of the place you want, which you can choose between the list of option shown. <br> 
![image](https://user-images.githubusercontent.com/85867861/177568493-02c8c6ae-fffb-4af1-b467-3d4155e429bf.png)
<br>
<br>
**There are also slash commands:** <br>

To create a slash command you have to go to [this link](https://api.slack.com/apps) and create them following the instruction given (try to be as brief as possible in yor descriptions of the commands or they won't be fully readable). <br>
Then in order to use them you first need to create a server, and the url of the server will be the one you will put in your slash command (in the "Request URL" field when you create one). <br>

In order to do this I used [ngrok](https://ngrok.com/docs/getting-started). <br>
In order to activate it in local you first need to install it, you can follow  [this link](https://ngrok.com/download), or if you use window you can do it from the terminal by typing, (make sure to install in in the right folder, I installed it in \Lunch_Organizer_Bot, so to move in that folder I typed cd in the terminal and then the path for that folder): <br>
`choco install ngrok` <br>

Then you should make an [account on ngrok](https://ngrok.com/product), get your [Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken) and type: <br>
`ngrok config add-authtoken <token>` <br>

And you should repalce `<token>` with your authtoken. <br>
Then you can start ngrok, make sure that you are in the right folder.You can start it on the port you want, which has to be the same as the one of your program, (I used the port 5000): <br>
`ngrok http 5000` <br>

After that, you get a link (which will be different each time if you use the free version of ngrok, so if you restart the server you will need to substitute the link each time), which you can paste in the "Request URL" field when creating a slash command: <br> 
<img width="522" alt="image" src="https://user-images.githubusercontent.com/85867861/177743709-2b1b99e4-7a35-4b27-9353-28f0ab10ce17.png"> <br>

Lets look at each slash command: <br>
First command: `/list_lunch_places` <br>
This command allows you to see a table containing all the info about the restaurants that are in the file with all the restaurants suggestions. And if you type "raw" after the command it will send you the raw file in the direct chat you have with the bot. <br>
To create this slash command type `/add_row` in the "Command" field when you create it, and in the URL field, after you have written your ngrok URL type ".../list_lunch_places". <br>
<br>
Second command: `/add_row` <br>
Then this command will allow you to add a new row to the file with all the restaurants suggestions. The bot will first check if the information provided are in the right format. If they aren't it will tell you to put them in the right format (you can see the actual file and take it as a reference). <br>
To create this slash command type `/add_row` in the "Command" field when you create it, and in the URL field, after you have written your ngrok URL type ".../add_row". <br>
<br>
Third command: `/remove_row` <br>
This command instead allows you remove a specific row from the file with all the restaurants suggestions, you just need to type, after the command, the number of the row you want to remove. <br>
To create this slash command type `/remove_row` in the "Command" field when you create it, and in the URL field, after you have written your ngrok URL type ".../remove_row". <br>
<br>
<br>

## How to run your bot on Raspberry Pi and use a SSH to program it.

First thing you need to do is take your Raspberry pi and install on it an OS. <br>
See [the official documentation](https://www.raspberrypi.com/documentation/computers/getting-started.html) for more info. <br>

After you configure it you need to know its IP adress (check again the previous link). <br>
So after you pluged-in the Raspberry Pi, you attached it to the lan, or gave it access to the wifi network and if the device is near your computer, only then you can run the following code on your terminal, with the respectivee IP adress: <br>
example <br>
`ssh pi@67.543.345.65` <br>
or if it is not renamed or you don't know the IP<br>
`ssh pi@raspberrypi.local` <br>
The first time it will ask you if you are sure and you want to continue, you can answer "yes". <br>
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
45 12 * * 0-5 ~/request2.sh
10 13 * * 0-5 ~/request1.sh
```
Here you can write all the right names of your file, including the one that starts at every reboot and the other for three messages. <br> 
Then you can select the time you prefer by writing first the minutes and then the hour at which you want your bot to send the message. So in my case I decided to send my messages at `12:00`, `12:30` and `13:10` (the preview photo created appositely not at any specific time). And then you can select also which day of the week the bot should send the message. I chose from monday to friday, so `0-5`. For more info on how to specify when to send the message this is what the values should be in order (as it is said in the editor): <br>
1. m - Minute - 0 through 59
2. h - Hour - 0 through 23
3. dom - Day of Month - 0 through 31
4. mon - Month - 0 through 12
5. dow - Day of Week - 0 through 7 (0 and 7 are both Sunday)

(asterisk means always) <br>
Then you can close the editor. <br>

In order to activate ngrok on your Raspberry you need to go in the folder you prefer and type: <br>
```
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
```

(rmember that here we are on Linux) <br>
Then you need to insert your authtoken, (the same as the one before):
`./ngrok config add-authtoken <token>` <br>

And finally you can strat ngrok at the port you want, (just like on windows): <br>
`./ngrok http 5000` <br>

And also this time you will need to rewrite the link you get in the slash commands, (look in the previous explanation).

If you want now you can do a reboot by typing: <br>
`sudo reboot` <br>
After that your Raspberry Pi should be ready to go! When you want to use it you just need to plug it in.
And if you want connect again to it just type the first command we typed before to connect: <br>
`ssh pi@67.543.345.65` <br>
Just remember to use the right IP adress, or if it is not renamed or you don't know the IP you can also write: <br>
`ssh pi@raspberrypi.local` <br>
