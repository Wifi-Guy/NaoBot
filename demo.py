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

usevid = True

class multibot:
    '''Creates a bot class to differentiate bots and pass items through from upgradedBot'''
    
    def __init__(self, robotip, colour):
        self.robotip = robotip
        self.colour = colour

    def video(self):
        try:
            ViewVideo(robotip=self.robotip).run(imagename=self.colour)
        except Exception, e:
            print(str(e))

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

def vidcontrol(tkinst):
    try:
        for item in tkinst.slaves():
            item.destroy()
        showBlue = ImageTk.PhotoImage(
            Image.open(
            "blue.jpg").resize((640, 480), Image.ANTIALIAS))
        showRed = ImageTk.PhotoImage(
            Image.open(
            "red.jpg").resize((640, 480), Image.ANTIALIAS))
        w = Label(tkinst, 
            image=showBlue) # TODO WITH MULTIPLE BOTS RUNNING DEMO DOESNT WORK
        x = Label(tkinst, 
            image=showRed)
        w.image = showBlue
        x.image = showRed

        w.pack()
        x.pack()
        tkinst.update()
    except Exception, e:
        print(str(e))

vidBot = [blue,red]



def vid(tkinst):
    #try:
    while True:
        for i in vidBot:
            i.video()

        vidcontrol(tkinst)
    #except:
    #    pass

def redtodo():
    try:
        '''Enter code for red down here'''
       # red.stand()
        #for x in range(0,2):
        #red.move(1)#0.00625)
        pass

        #red.stand()
        #red.demo()
        #red.follow()
    except:
       pass

def bluetodo():
    try:
        '''Enter code for blue down here'''

        blue.stand()
        #blue.move(1)
        #blue.demo()
        #blue.follow()
    except:
        pass

class myThread(threading.Thread):
    '''creates threads for use'''
    def __init__(self, threadID, colour, tkinst = None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.colour = colour
        self.tkinst = tkinst
    def run(self):
        if self.colour == "video":
            vid(tkinst)
        if self.colour == "red":
            redtodo()
        elif self.colour == "blue":
            bluetodo()


if __name__ == "__main__":
    if usevid:
        tkinst = Tk()
        thread0 = myThread(0, "video", tkinst)
        thread1 = myThread(1, "red")
        thread2 = myThread(2, "blue")
    else:
        thread1 = myThread(1, "red")
        thread2 = myThread(2, "blue")

    thread0.start()
    thread1.start()
    thread2.start()
    
    thread0.join()
    thread1.join()
    thread2.join()
