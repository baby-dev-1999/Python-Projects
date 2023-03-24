import datetime
import pywhatkit
from requests import get
import speech_recognition as sr
import pyttsx3
import pyjokes
import cv2
import webbrowser
import wikipedia
import random
import wolframalpha
import os
from pywhatkit import *
import smtplib
from email.message import EmailMessage

#speech engine initialisation
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
activationWord = 'danny'

#configuring Browser
#set the path
brave_path =r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))

#Wolfram Alpha Client
appid = 'GHYUTQ-4XVK98U7Q5'
wolframClient = wolframalpha.Client(appid)

def speak(text, rate = 150):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    print('Listening...')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print('recognizing')
        query = listener.recognize_google(input_speech, language = 'en_gb')
        print('The input was:', query)
    except Exception as exception:
        print('I did not get it bro can you repeat again..')
        speak('I did not get it bro, can you repeat again..')
        print (exception)
        return 'None'
    return query

#the result from Wolfarm may be in the form of list or a dictonary so we are creating this class
def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']
    
def search_wolframAlpha(query = ''):
    response = wolframClient.query(query)

    # @success = Wolfram able to give the result of query
    # @numpods = Many results were returned like google results
    # in that Numpods there were pods and subpods sorted in the order of highest confidence
    # we need to return the highest confident pods i.e, first pods or numpods
    if response['@success'] == 'false':
        return 'Could not compute your query bro'
    
    #query Resolved
    else:
        result = ''
        #question
        pod0 = response['pod'][0] #contains original question
        pod1 = response['pod'][1] # May contain the answer if it has the highest confidence value

        # if the result contains the title element then it is the answer (or)
        # if the result is primary result in wolfarm acording confidence value it is the answer (or)
        # if the result contains the defnition of our question then it is the answer 
    
        if (('result') in pod1 ['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('defnition' in pod1['@title'].lower()):
            
            #get the result
            result = listOrDict(pod1['subpod'])# returns result if there are any
            #remove brackets from results
            return result.split('(') [0] # returns result if there are any
        else:
            question = listOrDict(pod0['subpod'])# returns the question itself if there are no results
            #remove brackets from results
            return question.split('(') [0]# returns the question itself if there are no results
        
            #searching wikipedia for the same question as it has already returned the question
            speak('computation failed bro')
            speak(' Now searching universal databank for you')
            return search_wikipedia(question)
    
#main loop
if __name__ == '__main__':
        speak('Hello bro, What Do want Me to Do.')

        while True:
            #parse as a list
            query = parseCommand().lower().split()

            if query [0] == activationWord:
                query.pop(0)

                #listing commands
                if query[0] == 'say':
                    if 'hello' in query:
                        speak('hello bro')
                    else:
                        query.pop(0)#putting that poped out elemnt into list and repeating the instruction we gave
                        speech = ' '.join(query)#syntax to put back the popped out element into the query listen
                        query = str(query)
                        speak(query)

                #youtube
                if query[0] == 'play':
                    query = ' '.join(query[1:])
                    speak('playing ' + query)
                    pywhatkit.playonyt(query)

                #navigation
                if query[0] == 'search':
                    speak('opening...')
                    query = ' '.join(query[1:])
                    webbrowser.get('brave').open_new(query)

                #openingNotepad
                if query[0] == 'open' and query[1] == 'notepad':
                    npath = "C:\Windows\\notepad.exe"
                    os.startfile(npath)

                #openCMD
                if query[0] == 'open' and query[1] == 'command' and query[2] == 'prompt':
                    os.system("start cmd")

                #wikipedia
                if query[0] == 'do' and query[1] == 'you' and query[2] == 'know':
                    try:
                        speak('Serching the web bro.')
                        query = ' '.join(query[3:])
                        info = wikipedia.summary(query, 3)
                        print(info)
                        speak(info)
                    except:
                        speak('Sorry bro i found nothing in web')
                
                #time
                if 'time' in query:
                    time = datetime.datetime.now().strftime('%I:%M %p')
                    speak('Current time is ' + time)
                
                #date
                if 'date' in query:
                    now = datetime.datetime.now()
                    print('Date', now.strftime ("%Y-%m-%d"))
                    speak(now.strftime("%Y-%m-%d"))
                    speak('is the date today')

                #Wolfram Alpha
                if query[0] == 'using' and query[1] == 'wolf':
                    query = ' '.join(query[2:])
                    speak('computing your query bro, wait a second for results.')
                    try:
                        result = search_wolframAlpha(query)
                        speak(result)
                    except:
                        speak('unable to compute bro.')

                #open camera
                if query[0] == 'open' and query[1] == 'camera':
                    cap = cv2.VideoCapture(0)
                    while True:
                        ret, img = cap.read()
                        cv2.imshow('webcam', img)
                        k = cv2.waitKey(50)
                        if k == 27:
                            break;
                    cap.release()
                    cv2.destroyAllWindows()

                #playing Music
                if query[0] == 'start' and query[1] == 'music':
                    music_dir = "C:\\Users\\talla\\OneDrive\\Desktop\\old songs"
                    songs = os.listdir(music_dir)
                    rd = random.choice(songs)
                    os.startfile(os.path.join(music_dir, rd))  
                
                #note taking
                if query[0] == 'take' and query[1] == 'log':
                    speak('Ready to take your log bro')
                    newNote = parseCommand().lower()
                    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    with open ('note_%s.txt' %now, 'w') as newFile:
                        newFile.write(newNote)
                    speak('Note Written')

                #opening social media accounts
                # here you can add multiple account like facebook, twitter, stackoverflow and github etc.
                if query[0] == 'open' and query[1] == 'insta':
                    webbrowser.open("www.instagram.com")

                #for searching a particular thing in google or chrome or any web browser
                if query[0] == 'open' and query[1] == 'google':
                    speak('sir, what should i search for')
                    cmd = parseCommand().lower()
                    webbrowser.open(f"{cmd}")

                #tellingjoke
                if 'joke' in query:
                    speak(pyjokes.get_joke())

                #sending whats app message
                if query[0] == 'send' and query[1] == 'whatsapp':
                    speak('Tell me the number, to which i have to send whatsapp')
                    num = parseCommand().lower()
                    speak('what message do you want me to send')
                    msg = parseCommand().lower()
                    speak('at what time do you want me to send the message')
                    print('it is always advisable to give 2 minutes prior time for whatsApp to load')
                    time = input('Enter time in (HH:MM) FORMAT :')
                    time = time.split(':')
                    hrs = int(time[0])
                    min = int(time[1])
                    print(time[0], time[1])
                    print(hrs, min)
                    pywhatkit.sendwhatmsg(f"+91+{num}", f"{msg}",hrs,min)

                # Sending mail via our own SMTP server
                if query[0] == 'send' and query[1] == 'mail':
                    speak('give me the recipient mail id')
                    to = input('give me the mail id : ')
                    speak('what is the subject of your mail')
                    sub = parseCommand().lower()
                    speak('what message do you want me to send')
                    content = parseCommand()
                    msg = EmailMessage()
                    msg.set_content(f'{content}')
                    msg['Subject'] = sub
                    msg['From'] = "tpyt119@gmail.com"
                    msg['To'] = to
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login('tpyt119@gmail.com','bxhisfunsfkwcsko')
                    server.send_message(msg)
                    speak('Your Email has been sent sucessfully.')

                #if user gives some random question it wiil open web just like google assistant
                if query[0] == 'who' or query[0] == 'what' or query[0] == 'where' or query[0] == 'why' or query[0] == 'which' or query[0] == 'when' or query[0] == 'whose' or query[1] == 'whom' or query[0] == 'how':
                    speak('here is what i found on web')
                    query = ' '.join(query[2:])
                    query = str(query)
                    query = 'https://www.google.com/search?q='+query
                    webbrowser.get('brave').open_new(query)
                  
                #exit
                if query[0] == 'go' and query[1] == 'to' and query[2] == 'sleep':
                    speak('GoodBye bro, Have a great day')
                    break

                    

                    

