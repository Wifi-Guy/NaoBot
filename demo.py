'''demo test of both bots running together'''
import threading
from upgradedBot import *
from PIL import Image, ImageTk
from Tkinter import Tk

#TODO time sleep in bot
BLUEIP = "192.168.1.146"#Theyll need editing lol
REDIP = "192.168.1.145"
STAYVID = True
redvidc = True
bluevidc = True

usevid = True

class multibot:
    '''Creates a bot class to differentiate bots and pass items through from upgradedBot'''
    
    def __init__(self, robotip, colour):
        self.robotip = robotip
        self.colour = colour

    def video(self):
        print("videorunn")
        ViewVideo(robotip=self.robotip).run(imagename=self.colour)

    
    def vidcontrol(self, tkinst):
        print("vidcrunn")
        try:
            showBlue = ImageTk.PhotoImage(
                Image.open(
                "blue.jpg").resize((640, 480), Image.ANTIALIAS))
            showRed = ImageTk.PhotoImage(
                Image.open(
                "red.jpg").resize((640, 480), Image.ANTIALIAS))
        except Exception, e:
            print(str(e))
        #try:
        w = Label(tkinst, 
            image=showBlue) # TODO WITH MULTIPLE BOTS RUNNING DEMO DOESNT WORK
        x = Label(tkinst, 
            image=showRed)
        w.image = showBlue
        x.image = showRed

        w.pack()
        x.pack()
        tkinst.update()

    def move(self,distanceForward):
        AdvancedMovement(robotip=self.robotip).move(distanceForward,0)

    def follow(self):
        FollowBall(robotip=self.robotip).run()
    
    def tts(self, text):
        '''Text to speech pass through'''
        TextToSpeech(robotip=self.robotip).run(text)
    
    def demo(self):
        Demonstrations().alltogethernow(self.robotip)
    
    def stand(self):
        AdvancedMovement(robotip=self.robotip).onoff(True)
    
    def sit(self):
        AdvancedMovement(robotip=self.robotip).onoff(False)
    
    def walk(self, distanceforward, distanceleft, angle=0):
        AdvancedMovement(robotip=self.robotip).move(distanceforward, distanceleft, angle)

blue = multibot(BLUEIP, "blue")
red = multibot(REDIP, "red")

def redvid(tkinst):
    #try:
    while True:
        for item in tkinst.slaves():
            item.destroy()
        red.video()
        red.vidcontrol(tkinst)
    #except:
    #    pass

def bluevid(tkinst):
    #try:
    while True:
        blue.video()
        blue.vidcontrol(tkinst)
    #except:
    #    pass

def redtodo():
    try:
        '''Enter code for red down here'''
        #red.move(1)
        #red.sit()
        #red.stand()
        #red.demo()
        #red.follow()
        pass
    except:
       pass

def bluetodo():
    try:
        '''Enter code for blue down here'''
        #blue.move(1)
        #blue.stand()
        #blue.demo()
        #blue.follow()
        pass
    except:
        pass

class myThread(threading.Thread):
    '''creates threads for use'''
    def __init__(self, threadID, colour, video=False, tkinst = None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.colour = colour
        self.video = video
        self.tkinst = tkinst
    def run(self):
        if self.video:
            if self.colour =="red":
                redvid(self.tkinst)

            elif self.colour == "blue":
                bluevid(self.tkinst)

        else:
            if self.colour == "red":
                redtodo()
            elif self.colour == "blue":
                bluetodo()


if __name__ == "__main__":
    if usevid:
        tkinst = Tk()
        thread1 = myThread(1, "red", True, tkinst)
        thread2 = myThread(2, "blue", True, tkinst)
    else:
        thread1 = myThread(1, "red")
        thread2 = myThread(2, "blue")
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
