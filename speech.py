import speech_recognition as sr
import pyttsx3

listener = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        mic_index = 0
        with sr.Microphone(device_index=mic_index) as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)
            audio = listener.listen(source, timeout=5, phrase_time_limit=10)
            command = listener.recognize_google(audio)
            command = command.lower()
            print("You:", command)
            return command
    except Exception as e:
        speak("Sorry, I didn't catch that.")
        print("Error:", e)
    return None
