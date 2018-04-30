# NaoBot
## upgradedBot

**Dependencies**

To run this code, it is required to have:

datetime, time, Image, vision_definitions. PIL, Tkinter, wit,difflib

Note that most of these are already built into Python2, however it is recommended to use Anaconda (this project was created using Anaconda 4.4.0)

This project will also need naoqi to interface with the bot, which is available at http://doc.aldebaran.com/2-4/dev/python/install_guide.html#python-install-guide
with an Alderban account

**Code Functions**

These are the code functions of the upgradedBot program:

```Demonstrations```

Provides a basic set of demonstrations that the bot can use:

  ```startup``` Moves the bot to a basic startup position
  
  ```shutdown``` Move the bot to a shutdown position
  
  ```lightshow``` demonstrates the lights on the bot
  
  ```playmusic``` plays the previous piece of music played (will throw an error if no previous piece of music has been played)
  
  ```brainleds``` demonstrates the LEDs on the bots head
  
  ```speaking``` says any word typed into the console, with ```sys_help``` reading a help text, ```cur_bat``` reading the current battery, ```kill_sys``` stopping the text to speech, and ```cur_time``` reading out the current time
  
  ```voicerecognition``` will reply to ```"hello","Matthew","Goodbye", and "battery"```
  
  ```viewVideo``` opens a Tkinter window and streams video from the bot
  
  ```alltogethernow``` gives a demonstration of the connected space
  
  ```entrance``` the bot will ask people their names and then greet them at the entrance, about 80% accurate

Any of these pieces of code can be ran by importing upgradedBot and running them:

```
from upgradedBot import *

demonstrations().alltogethernow()
```

will run the demonstrations code

The other functions that are not part of the demonstrations section are below:

Movement control contains a program for moving individual limbs or walking

Walking control is done using ```AdvancedMovement().move(forward,left,angle=0)``` where all three variables can be either positive or negative to move

Individual limb control is done using ```AdvancedMovement().run(movementList, speed=0.2)``` movement list is a 2d list, where the first variable is either an integer or a motor, and the second variable is the angle you wish to move the bots arm to in radians. *It is also highly recommended not to change the speed, as putting the speed too high risks the bot falling over and breaking*

An advanced function using movement control is Follow Ball, where the bot will follow a small red ball around a given space
*This code is experimental and liable not to work, it work about 50% of the time in a controlled environment*
The code is ran using ```FollowBall().run()``` where it will immediately ran, so it is recommended to add a delay before start to get into the correct position

LED changer is a function that changes the colour of certian LEDs on the bots body for a specified length of time.
This code runs the same way as all other code, using ```LEDChanger().run(ledlist=None, changetime=5)``` where ledlist is a 2d array which first variable is either an led name or its led reference number, and the second being the intensity of the led.

The bots can also play audio files that are sent to them, which is why play music was created. Play music can be activated using ```PlayMusic().run(musiclocation="Dean-Martin-Let-it-Snow.wav, robotip=DEFAULT_IP, port=9559)``` where musiclocation is the relative or absolute location of the file on the system *dean martins let it snow will not work as the file is not provided*

The bot also supports text to speech functionality, which makes up the majority of its human interaction. This can be ran by ```TextToSpeech().run(text)``` where text is any text except for ```sys_help``` which will read a help text, which will ```cur_bat``` read the current battery, which will ```kill_sys``` stop the text to speech, and which will ```cur_time``` read out the current time.

The bot supports streaming video from the cameras on it. This is done using ```ViewVideo().run()``` which will create a tkinter instance displaying images streamed off the bot at an approximately 0.3 second delay

The bot supports voice recording and voice recognition, however the voice recognition is spotting based, meaning that the command will only trigger on certian words. This can be used with ```VoiceRecognition().run(vocabulary, wordspotting=False, waittime=3)``` which will change the global NAME if a word is detected. Due to issues with this one, a more advanced one using getting audio and sending it off to an external server was devised, called voice get. This can be initialised using ```VoiceGet().run(wordlist=None, sleepTime=5, robotip=DEFAULT_IP, port= 9559)```. which will get audio, stream it to an external free service called wit and return a list of words found

****Texttospeech is a newer addition with working tts capabilities****

This works using the wit based voice get system, however using difflib to differentiate between words accurately. Please note it will not differentiate in some scenarios, for example if "dale" is said, but "alex" is written in the detect list, the program will trigger on alex, which is impossible to easily fix

## Demo

**Dependencies**

To run this code, you are required to have:

threading, upgradedBot, PIL and Tkinter as well as all the dependicies listed in upgradedBot

**Code Functions**

This program extends upgradedBot to allow for use with multiple bots and remote control.

It uses a class containing all of the imported commands from upgradedBot, which are:

```video()``` - allows video control, ```follow()``` - allows following the ball, ```tts()``` - text to speech, ```demo()``` - the demo of the connected space, ```stand()``` - makes the bot stand up, ```sit()``` - makes the bot sit down, ```walk()``` - moves the bot forward backward left and right

More advanced information about these is available in upgradedBot

Video control uses a single Tkinter frame and gets the images to show both the bots working at the same time

To put code for the bots to do simultaneously, but them in ```bluetodo()``` and ```redtodo()```
