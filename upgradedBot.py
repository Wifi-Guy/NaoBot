'''
Upgrades on NaoBot API with a more user friendly and logical middleware
'''
import datetime
import time
import vision_definitions
from PIL import Image, ImageTk
from Tkinter import Tk, Label
from wit import Wit

from naoqi import ALModule

DEFAULT_IP = "192.168.1.106"
#DEFAULT_IP = "169.254.65.171"

NAME = None
GETVOICE = None


class UpgradedBot():
    '''creates all the instances of ALBroker and ALProxy as parts of itself'''
    # pylint: disable=too-many-instance-attributes
    # All are required in this case

    def __init__(self,  robotip=DEFAULT_IP, port=9559):
        '''
        :param robotip: ip of bot
        :type: string

        :param port: port of bot on ip
        :type: int
        '''
        self.robotip = robotip
        self.mybroker = __import__("naoqi").ALBroker("mybroker", "0.0.0.0", 0, robotip, port)
        self.motionproxy = __import__("naoqi").ALProxy("ALMotion", robotip, port)
        self.ledproxy = __import__("naoqi").ALProxy("ALLeds", robotip, port)
        self.batteryproxy = __import__("naoqi").ALProxy("ALBattery", robotip, port)
        self.texttospeechproxy = __import__("naoqi").ALProxy("ALTextToSpeech", robotip, port)
        self.audiorecorderproxy = __import__("naoqi").ALProxy("ALAudioRecorder", robotip, port)
        self.audioproxy = __import__("naoqi").ALProxy("ALAudioPlayer", robotip, port)
        self.voicerecognitionproxy = __import__("naoqi").ALProxy("ALSpeechRecognition", robotip,
                                                                 port)
        self.vidproxy = __import__("naoqi").ALProxy("ALVideoDevice", robotip, port)
        self.photocapproxy = __import__("naoqi").ALProxy("ALPhotoCapture", robotip, port)
        self.memory = __import__("naoqi").ALProxy("ALMemory")


class TextToSpeech(UpgradedBot):
    '''enter text or command'''

    @staticmethod
    def help():
        '''returns basic help text for the class'''
        return'''
        run()
            sys_help - reads this help text
            cur_bat  - reads current battery
            kill_sys - stops system
            cur_time - reads current time
            bot will say all other text
        '''

    def run(self, text):
        '''
        :type string text: bot will say entered text unless a command is said
        :commandList
        -cur_bat- reads current battery
        -kill_sys- stops system
        -cur_time_ reads current time
        '''
        if str(text[:7]) == str("cur_bat"):
            self.texttospeechproxy.say("Battery"+str(self.batteryproxy.getBatteryCharge())+"%")
        elif str(text[:8]) == str("kill_sys"):
            return False
        elif str(text[:8]) == str("cur_time"):
            self.texttospeechproxy.say("The current time is "+str(datetime.datetime.now().minute)
                                       + "minutes past"+(str(datetime.datetime.now().hour)
                                                         if str(datetime.datetime.now().hour)
                                                         < "13" else str
                                                         (datetime.datetime.now().hour-12)))
        elif str(text[:8]) == str("sys_help"):
            print(self.help())
        else:
            self.texttospeechproxy.say(text)
        return True


class LEDChanger(UpgradedBot):
    '''Changes LEDs'''

    def run(self, ledlist=None, changetime=5): # main program to run
        '''
        :param ledlist: 2d list of leds to change,
        first item being LED NAME and second being intensity,
        example [("LeftFaceLedsRed",0.1),(0,0.1)]
        :type: 2dlist

        :param changetime: float time that the leds will change colour for
        :type: float
        '''

        if ledlist is None:
            #self.ledproxy.rasta(changetime)
            #self.ledproxy.randomEyes(changetime)
            self.ledproxy.setIntensity("LeftFaceLedsRed", 1)
            self.ledproxy.setIntensity("LeftFaceLedsGreen", 0)
            self.ledproxy.setIntensity("LeftFaceLedsBlue", 0)

            self.ledproxy.setIntensity("RightFaceLedsRed", 1)
            self.ledproxy.setIntensity("RightFaceLedsGreen", 0)
            self.ledproxy.setIntensity("RightFaceLedsBlue", 0)
            '''
            self.ledproxy.setIntensity("LeftFaceLedsRed", 0.407843137)
            self.ledproxy.setIntensity("LeftFaceLedsGreen", 0.0549019608)
            self.ledproxy.setIntensity("LeftFaceLedsBlue", 0.839215686)

            self.ledproxy.setIntensity("RightFaceLedsRed", 0.407843137)
            self.ledproxy.setIntensity("RightFaceLedsGreen", 0.0549019608)
            self.ledproxy.setIntensity("RightFaceLedsBlue", 0.839215686)'''
        else:
            for item in ledlist:
                if isinstance(item[0], int):
                    item[0] = self.ledproxy.listLEDs()[item[0]]
                self.ledproxy.setIntensity(item[0], item[1])

        time.sleep(changetime)
        for item in self.ledproxy.listLEDs():
            self.ledproxy.reset(str(item))

    @staticmethod
    def ledlist():
        '''A list of which LEDs are in which areas on the bot'''
        return
        '''
        The list of LEDs and which set it belongs to:
        brain=[0,1,2,3,4,5,6,7,8,9,10,11]
        chest=[12,13,14]
        leftEar=[15,16,17,18,19,20,21,22,23,24]
        leftFace=[25,26,27,28,29,30,31,32]
        leftFoot=[33,34,35]#RGB different LEDs
        rightEar=[36,37,38,39,40,41,42,43,44,45]
        rightFace=[46,47,48,49,50,51,52,53]
        rightFoot=[54,55,56]#RGB different LEDs
        '''

    @staticmethod
    def help():
        '''returns basic help text for the class'''
        return'''
        run()
            ledlist is a 2d array, which is a list of tuples. Each tuple should be size two, 
            where the first item is the LED number or its list and the second should be its intensity
            Example: [("LeftFaceLedsRed",0.1),(0,0.1)]
        ledlist()
            A list of which LEDs are in which areas on the bot
        '''


class AdvancedMovement(UpgradedBot):
    '''more advanced wrapper for movement'''

    def run(self, movementlist, speed=0.2): # a logical slightly simplified wrapper for ALMotion
        '''
        :param movementlist: 2d list of movement items, example: [["LElbowYaw",0.2],[8,0.2]]
        :type movementlist: 2dlist

        :param speed: bot movement speed
        type speed: float
        '''
        jointarray = ["HeadYaw", "HeadPitch", "LShoulderPitch", "LShoulderRoll",
                      "LElbowYaw", "LElbowRoll", "LWristYaw", "LHipYawPitch",
                      "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch",
                      "LAnkleRoll", "RHipYawPitch", "RHipRoll", "RHipPitch",
                      "RKneePitch", "RAnklePitch", "RAnkleRoll", "RShoulderPitch",
                      "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "LHand", "RHand"]
        jointlist = []
        jointangle = []
        for item in movementlist:
            if isinstance(item[0], int):
                item[0] = jointarray[item[0]]
            jointlist.append(item[0])
            jointangle.append(item[1])
        self.motionproxy.setAngles(jointlist, jointangle, speed)

    def onoff(self, turnon):
        '''turns the bot on or off'''
        if turnon:
            self.motionproxy.wakeUp()
        else:
            self.motionproxy.rest()

    @staticmethod
    def jointlist():
        '''returns a full list of joints with number equivelants'''
        return
        '''
        This is the comprehensive list of joints for the Nao Bot
        0:HeadYaw
        1:HeadPitch
        2:LShoulderPitch
        3:LShoulderRoll
        4:LElbowYaw
        5:LElbowRoll
        6:LWristYaw
        7:LHipYawPitch
        8:LHipRoll
        9:LHipPitch

        10:LKneePitch
        11:LAnklePitch
        12:LAnkleRoll
        13:RHipYawPitch
        14:RHipRoll
        15:RHipPitch
        16:RKneePitch
        17:RAnklePitch
        18:RAnkleRoll
        19:RShoulderPitch

        20:RShoulderRoll
        21:RElbowYaw
        22:RElbowRoll
        23:RWristYaw
        24:LHand
        25:RHand
        '''

    @staticmethod
    def help():
        '''returns basic help text for the class'''
        return '''
        run() - main program
            This is a logical wrapper for ALMotion
            It uses the words from ALMotion, however these are then paired with an absolute angle to rotate them too
            Example:
            [["LElbowYaw",0.2],["LHipRoll",0.5]] - rotates Left elbow yaw to 0.2 and Left hip roll to 0.5
        onoff()
            This function turns the bots movement sytem on and off
        jointlist()
            This is the list of joints and their number
        '''


class VoiceGet(UpgradedBot):
    '''returns a voice file from 5 seconds of recording
    Not 100% working, online API doesnt like names or
    too much background noise'''

    def run(self, wordList=None, sleepTime=5, robotip=DEFAULT_IP, port=9559):
        '''Records audio, sends the audio to wit and returns the text'''
        client = Wit("UAWHDAJAR6GF6M7S7EA43OAO7KPUO4WW")
        self.audiorecorderproxy.startMicrophonesRecording("/var/persistent/home/nao/recordFile.wav",
                                                          "wav", 16000, [0, 0, 1, 0])
        time.sleep(sleepTime)
        self.audiorecorderproxy.stopMicrophonesRecording()
        session = __import__("ftplib").FTP(robotip, "nao", "nao")
        session.retrbinary("RETR recordFile.wav", open("recordFile.wav", "wb").write)
        start = time.time()
        with open("recordFile.wav", "rb") as f:
            resp = client.speech(f, None, {"Content-Type":"audio/wav"})
        resp = (str(resp).split("_text': u")[1])[1:-2]
        if wordList is None:
            return resp
        returnList = []
        for item in str(resp).split(" "):
            if isinstance(item, wordList):
                returnList.append(item)
        return returnList


class VoiceRecognition(UpgradedBot):
    '''on word detection, the GetUserVoice object gets activated
    #TODO voice recognition not working'''

    def run(self, vocabulary, wordspotting=False, waittime=3):
        '''Runs the program'''
        print("TEST")
        try:
            self.voicerecognitionproxy.pause(True)
            self.voicerecognitionproxy.setVocabulary(vocabulary, wordspotting)
            self.voicerecognitionproxy.pause(False)
        except BaseException:
            print("ERR_VOCAB:voicerecognition-run")
        try:
            self.voicerecognitionproxy.subscribe("recognisedWord")
        except BaseException:
            print("ERR1:voicerecognition-run")
        try:
            global GETVOICE
            if GETVOICE is None:
                GETVOICE = GetUserVoice("GETVOICE")
            time.sleep(waittime)
        except BaseException:
            print("ERR_GLOBAL:voicerecognition-run")
        try:
            self.memory.unsubscribeToEvent("WordRecognized", "GETVOICE")
        except BaseException:
            print("ERR_EVENT:voicerecognition-run")
        try:
            self.voicerecognitionproxy.unsubscribe("recognisedWord")
        except BaseException:
            print("ERR_UNSUB:voicerecognition-run")
        try:
            GETVOICE = None
        except BaseException:
            print("ERR_DEL:voicerecognition-run")
        return True

    def unsub(self):
        '''tries to unsubscribe all events from bot'''
        try:
            self.memory.unsubscribeToEvent("WordRecognized", "GETVOICE")
            print("UNSUB:VR-UNSUB")
        except BaseException:
            print("ERR_EVENT:voicerecognition-unsub")
        try:
            self.voicerecognitionproxy.unsubscribe("recognisedWord")
        except BaseException:
            print("ERR_UNSUB:voicerecognition-unsub")


class GetUserVoice(ALModule):
    '''This is a ALModule python object **DO NOT USE**'''

    def __init__(self, NAME):
        ALModule.__init__(self, NAME)
        try:
            upgradedBot().memory.unsubscribeToEvent("WordRecognized", "GETVOICE")
            print("UNSUB:GUV-init")
        except BaseException:
            print("ERR_EVENT:GUV-init")
        upgradedBot().memory.subscribeToEvent("WordRecognized", "GETVOICE", "onwordrecognized")

    @staticmethod
    def onwordrecognized(event, value, other):
        '''changes global name to recognised word'''
        global NAME
        NAME = value[0]

    @staticmethod
    def unsub():
        '''unsubcribes event from bot'''
        try:
            upgradedBot().memory.unsubscribeToEvent("WordRecognized", "GETVOICE")
            print("UNSUB:GUV-unsub")
        except BaseException:
            print("ERR_EVENT:GUV-unsub")


class ViewVideo(UpgradedBot):
    '''views stream from bots TODO doesnt work
    image function/open tkinter doesnt work'''

    def run(self, robotip=DEFAULT_IP, port=9559):  # Opens a tkinter window showing application
        '''
        :param robotip: ip of bot
        :type: string

        :param port: port of bot on ip
        :type: int
        '''
        root = Tk()
        root.geometry("1000x1000")
        self.photocapproxy.takePicture("/var/persistent/home/nao", "image.jpg")
        session = __import__("ftplib").FTP(robotip, "nao", "nao")
        session.retrbinary("RETR image.jpg", open("image.jpg", "wb").write)
        while True:
            for item in root.slaves():
                item.destroy()
            self.photocapproxy.takePicture("/var/persistent/home/nao", "image.jpg")
            #time.sleep(0.2)
            session = __import__("ftplib").FTP(robotip, "nao", "nao")
            session.retrbinary("RETR image.jpg", open("image.jpg", "wb").write)
            showimage = ImageTk.PhotoImage(Image.open("image.jpg"))
            w = Label(root, image=showimage)
            w.image = showimage
            w.pack()
            root.update()


class PlayMusic(UpgradedBot):
    '''Plays music'''

    def run(self, musiclocation="Dean-Martin-Let-it-Snow.wav",
            robotip=DEFAULT_IP, port=9559):
        '''
        :param musiclocation: location of music file on system
        :type: string

        :param robotip: ip of bot
        :type: string

        :param port: port of bot on ip
        :type: int
        '''
        session = __import__("ftplib").FTP(robotip, "nao", "nao")
        session.storbinary("STOR file.wav", open(musiclocation, "rb"))
        session.quit()
        temp = self.audioproxy.loadFile("/var/persistent/home/nao/file.wav")
        self.audioproxy.play(temp)


class Demonstrations:
    '''a small list of Demonstrations'''

    def __init__(self):
        pass

    @staticmethod
    def startup(saybat=True, ip=DEFAULT_IP):
        '''Runs basic startup sequence
        #moving the bot to idle active and reading out current battery level'''
        AdvancedMovement(robotip=ip).onoff(True)
        if saybat:
            TextToSpeech().run("cur_bat")

    @staticmethod
    def shutdown(saybat=True, ip=DEFAULT_IP):
        '''Runs shutdown sequence
        #moving the bot into balanced position and reading out battery level'''
        AdvancedMovement(robotip=ip).onoff(False)
        if saybat:
            TextToSpeech().run("cur_bat")

    @staticmethod
    def lightshow(ip=DEFAULT_IP):
        '''test leds then has speaking'''
        LEDChanger(robotip=ip).run(changetime=1)
        Demonstrations(robotip=ip).brainleds(1)
        Demonstrations(robotip=ip).speaking()

    @staticmethod
    def playmusic(ip=DEFAULT_IP):
        '''Plays let it snow as a demonstration'''
        PlayMusic(robotip=ip).run()

    @staticmethod
    def throw(ip=DEFAULT_IP):
        '''throws ball, WIP --TODO FIX'''

        AdvancedMovement(robotip=ip).run([["RHand", 1]])

        time.sleep(3)

        AdvancedMovement(robotip=ip).run([["RHand", -1]])

        time.sleep(3)
        AdvancedMovement(robotip=ip).run([["RShoulderRoll", 2]])
        AdvancedMovement(robotip=ip).run([["RShoulderPitch", 3], ["RWristYaw", 3]])

        time.sleep(1)

        AdvancedMovement(robotip=ip).run([["RHand", 1]])
        time.sleep(0.3)
        AdvancedMovement(robotip=ip).run([["RShoulderPitch", -2]], speed=1)
        AdvancedMovement(robotip=ip).run([["RElbowYaw", 3]])
        AdvancedMovement(robotip=ip).run([["RShoulderPitch", 3]])

    @staticmethod
    def brainleds(maxtime=5, ip=DEFAULT_IP):
        '''Makes the LEDs flash for 5 seconds then turns them off'''
        for _ in range(0, 10):
            templist = []
            for item in range(0, 12):
                templist.append([item, 0 if item%2 == 1 else 1])
            LEDChanger(robotip=ip).run(templist, maxtime/10)
            templist = []
            for item in range(0, 12):
                templist.append([item, 0 if item%2 == 0 else 1])
            LEDChanger(robotip=ip).run(templist, maxtime/10)
        templist = []
        for item in range(0, 12):
            templist.append([item, 0])
        LEDChanger(robotip=ip).run(templist, 0)

    @staticmethod
    def speaking(ip=DEFAULT_IP):
        '''says any commands until the kill word is said'''
        not_stop = True
        while not_stop:
            not_stop = TextToSpeech(robotip=ip).run(raw_input("Enter Text>>\n"))

    @staticmethod
    def voicerecognition(ip=DEFAULT_IP):
        '''detects hello, matthew, battery and goodbye
        #and does commands based on them'''
        cont = True
        VoiceRecognition(robotip=ip).run(["hello", "matthew", "goodbye", "battery"], waittime=5)
        global NAME
        while cont:
            if NAME is not None:
                time.sleep(2)
                print(NAME)
                if str(NAME)[6:-6] == "hello":
                    TextToSpeech().run("Hello, I am Nao")
                elif str(NAME)[6:-6] == "matthew":
                    TextToSpeech().run("Matthew is my programmer")
                elif str(NAME)[6:-6] == "goodbye":
                    TextToSpeech().run("Goodbye")
                    cont = False
                elif str(NAME)[6:-6] == "battery":
                    TextToSpeech(robotip=ip).run("cur_bat")
                VoiceRecognition(robotip=ip).run(["hello", "matthew", "goodbye"], True, 2)
                NAME = None

    @staticmethod
    def viewVideo(ip=DEFAULT_IP):
        '''views video with no other commands'''
        ViewVideo(robotip=ip).run()

    @staticmethod
    def powernap(ip=DEFAULT_IP):
        '''moves into shutdown position without shutdown **DOESNT WORK DO NOT USE**'''
        AdvancedMovement(robotip=ip).run([#["HeadYaw", -0.009246],["HeadPitch", 0.085862],
                                #["LShoulderPitch", 1.420442],["LShoulderRoll", 0.165630],
                                # ["LElbowYaw", -0.803858],
                                #["LElbowRoll", -1.058418],["LWristYaw", 0.136484],
                                # ["LHipYawPitch", -0.250000],
            ["LHipRoll", -0.082794], ["LHipPitch", -0.705598], ["LKneePitch", 2.112546],
            ["LAnklePitch", -1.189442], ["LAnkleRoll", 0.075016], ["RHipYawPitch", -0.250000],
            ["RHipRoll", 0.079810], ["RHipPitch", -0.701080], ["RKneePitch", 2.112546],
            ["RAnklePitch", -1.186300], ["RAnkleRoll", -0.075870], ["RShoulderPitch", 1.451206],
            ["RShoulderRoll", -0.170316], ["RElbowYaw", 0.797638], ["RElbowRoll", 1.047764],
            ["RWristYaw", -0.121228], ["LHand", 0.016800], ["RHand", 0.014000]])

    @staticmethod
    def alltogethernow(ip=DEFAULT_IP):
        '''demonstration of connected space'''
        tts = TextToSpeech(robotip=ip)
        move = AdvancedMovement(robotip=ip)
        Demonstrations().startup(False, ip=ip)
        print move.motionproxy.getAngles("Body", False)
        tts.run("Welcome to the Connect Space")
        time.sleep(0.2)
        move.run([["LShoulderRoll", 2], ["LShoulderPitch", -0.5], ["LElbowRoll", 2]])
        tts.run("This is the 3D printer")
        time.sleep(0.2)
        #3D printer
        move.run([["LShoulderRoll", 0.18377649784088135], ["LShoulderPitch", 1.470129132270813],
                  ["LElbowRoll", -0.4123087525367737]])
        move.run([["RShoulderPitch", 0.2],
                  ["RShoulderRoll", -0.5]])
        #Vive
        tts.run("And over here is the HTC vyve")
        time.sleep(0.2)
        move.run([["RShoulderPitch", 1.1925666332244873],
                  ["RShoulderRoll", 0.09999998658895493]])
        #
        move.run([["LShoulderRoll", 0.6], ["LShoulderPitch", 0], ["LElbowRoll", 2]])
        tts.run("And our newest addition to the connect space is the infr a red mouse, "
                "over there, connected to the smart board")
        time.sleep(0.3)
        Demonstrations().shutdown(False, ip=ip)

    @staticmethod
    def help():
        '''returns basic help text for the class'''
        return'''
        startup()
            Starts up the bots motors and reads the current battery
        shutdown()  
            Shuts down the bot and reads the current battery
        throw()
            Opens hand and throws any object placed in hand (TODO Currently)
        brainleds()
            Activates alternate LEDs on system, then cycles 10 times and turns all LEDs off
        speaking()
            Says entered text until kill command is given
        help()
            Returns this help information
        '''


def ttswork():
    '''demonstrates text to speech'''
    tts = TextToSpeech()
    voicerecog = VoiceRecognition()
    Demonstrations().shutdown()
    tts.run("Hello, I'm Nao, whats your NAME?")

    voicerecog.run(["Matt", "Tim", "Dale", "Also Tim"], waittime=5)##TODO giant list of names
    while NAME is None:
        pass
    tts.run(str("Hello "+NAME+" Welcome to the computing department"))

def main():
    '''Programs main, contains demo program + currently not working programs'''

    #ViewVideo().run()
    #AdvancedMovement().onoff(False)
    TextToSpeech().run("Test")
    AdvancedMovement().onoff(False)
    #Demonstrations().speaking()
    #print(VoiceGet().run())
    #Demonstrations().alltogethernow()

if __name__ == "__main__":
    main()
