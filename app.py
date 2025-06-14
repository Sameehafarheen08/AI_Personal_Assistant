from assistant.speech import take_command, speak
from assistant.tasks import handle_task

if __name__ == "__main__":
    speak("Hello Sameeha! I am your personal assistant. How can I help you today?")
    while True:
        command = take_command()
        if command:
            if "exit" in command or "stop" in command:
                speak("Goodbye Sameeha!")
                break
            else:
                handle_task(command)
