'''demo test of both bots running together'''
import threading
from upgradedBot import *

#TODO time sleep in bot

class multibot:
    '''Creates a bot class to differentiate bots'''
    
    def __init__(self, robotip):
        self.robotip = robotip
    
    def tts(self, text):
        '''Text to speech pass through'''
        TextToSpeech(robotip=self.robotip).run(text)
    
    def demo(self):
        Demonstrations().alltogethernow(self.robotip)
    
    def stand(self):
        AdvancedMovement(robotip=self.robotip).onoff(True)
    
    def sit(self):
        AdvancedMovement(robotip=self.robotip).onoff(False)
    
blue = multibot("192.168.1.106")
red = multibot("192.168.1.108")

def redtodo():
    '''Enter code for red down here'''
    red.demo()

def bluetodo():
    '''Enter code for blue down here'''
    blue.demo()

class myThread(threading.Thread):
    '''creates threads for use'''
    def __init__(self, threadID, colour):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.colour = colour
    def run(self):
        if self.colour == "red":
            redtodo()
        elif self.colour == "blue":
            bluetodo()


if __name__ == "__main__":
    thread1 = myThread(1, "red")
    thread2 = myThread(2, "blue")

    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
