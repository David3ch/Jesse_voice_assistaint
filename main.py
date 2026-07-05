import os
from pydoc import text
import time
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import datetime
import subprocess
import webbrowser

engine = pyttsx3.init()

lang = input("Enter the language code (en, ru): ")

if lang == 'en':
    engine.setProperty('voice', 'english')
elif lang == 'ru':
    engine.setProperty('voice', 'russian')


def speak(text):
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 100)  # Set the speech rate (optional)
    engine.setProperty('volume', 3.0)  # Set the volume (optional)


def get_audio():
    r = sr.Recognizer()

    if lang == 'en':
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            said = ''

            try:
                said = r.recognize_google(audio)
                print(said)

            except Exception as e:
                print("Exception: " + str(e))
    elif lang == 'ru':
        with sr.Microphone() as source:
            print("Слушаю...")
            audio = r.listen(source)
            said = ''

            try:
                said = r.recognize_google(audio, language='ru-RU')
                print(said)

            except Exception as e:
                print("Exception: " + str(e))

    
    return said.lower()

def note(text):
    date = datetime.datetime.now()
    filename = str(date).replace(":", "-") + "-note.txt"
    with open(filename, "w") as f:
        f.write(text)
    subprocess.Popen(["mousepad", filename])

def open_program(program_name):
    try:
        subprocess.Popen(program_name)
    except Exception as e:
        print(f"Failed to open {program_name}: {e}")

Wake_words = ['hey jessie', 'jessie', 'hey jessie', 'ok jessie', 'jessie wake up', 'wake up jessie', 'hello jessie', 'hi jessie']


NOTE_WORDS = ["make a note", "write this down", "remember this"]
PROGRAM_WORDS = ["open program", "launch", "run", "start", "open"]
PROGRAMS = {
    "telegram": "/snap/bin/telegram-desktop",
    "browser": "/usr/bin/google-chrome",
    "mousepad": "mousepad",
    "terminal": "xfce4-terminal",
    "code": "/snap/bin/code"
}



while True:
    print("Listening...")
    text_from_user = get_audio()


    if any(word in text_from_user for word in Wake_words):
        speak("Yes Mister White, how can I help you?")
        text_from_user = get_audio()

        if any(word in text_from_user for word in NOTE_WORDS):
            speak("What would you like me to write down?")
            note_text = get_audio()
            note(note_text)
            speak("I've made a note of that.")

        if any(word in text_from_user for word in PROGRAM_WORDS):
            speak("Which program would you like me to open?")
            program_name = get_audio()
            program_path = PROGRAMS.get(program_name)
            open_program(program_path)
            speak(f"Opening {program_name}.")
            if program_path == "/usr/bin/google-chrome":
                speak('What would you like me to search for?')
                search_query = get_audio()
                search_url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(search_url)

    if 'stop' in text_from_user or 'exit' in text_from_user:
        speak("Goodbye!")
        break


