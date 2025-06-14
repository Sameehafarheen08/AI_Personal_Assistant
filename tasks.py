import webbrowser
import datetime
import wikipedia
import pywhatkit
import requests
import pyjokes
import pyautogui
import cv2
import openai
from plyer import notification
from threading import Timer
from assistant.speech import speak
from assistant.config import WEATHER_API_KEY, OPENAI_API_KEY

def handle_task(command):
    if "time" in command:
        speak(datetime.datetime.now().strftime('%I:%M %p'))

    elif "date" in command:
        speak(datetime.datetime.now().strftime('%A, %B %d, %Y'))

    elif "who is" in command or "what is" in command:
        try:
            info = wikipedia.summary(command, sentences=2)
            speak(info)
        except:
            speak("Couldn't find information.")

    elif "play" in command:
        song = command.replace("play", "")
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif "weather" in command:
        get_weather()

    elif "joke" in command:
        speak(pyjokes.get_joke())

    elif "screenshot" in command:
        image = pyautogui.screenshot()
        image.save("screenshot.png")
        speak("Screenshot saved.")

    elif "remind me" in command:
        speak("What should I remind you?")
        task = input("Reminder: ")
        speak("In how many seconds?")
        delay = int(input("Seconds: "))
        Timer(delay, show_reminder, [task]).start()
        speak("Reminder set.")

    elif "face" in command:
        detect_face()

    elif "chat" in command or "question" in command:
        ask_chatgpt(command)

    else:
        speak("Sorry, I can't help with that yet.")

def get_weather():
    city = "Hyderabad"
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    try:
        data = requests.get(url).json()
        temp = data['current']['temp_c']
        condition = data['current']['condition']['text']
        speak(f"{temp}°C and {condition} in {city}")
    except:
        speak("Can't get weather info.")

def detect_face():
    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    speak("Looking for faces...")
    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
        cv2.imshow("Face Detection", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    speak("Stopped face detection.")

def ask_chatgpt(prompt):
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message['content']
        speak(reply)
    except Exception as e:
        speak("Error connecting to ChatGPT.")

def show_reminder(task):
    notification.notify(
        title='Reminder',
        message=task,
        timeout=10
    )
    speak(f"Reminder: {task}")
