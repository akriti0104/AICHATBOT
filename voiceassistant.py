import speech_recognition as sr
import pyttsx3
import csv
from datetime import datetime

# Initialize voice engine
engine = pyttsx3.init()

def speak(text):
    print("Jarvish:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You:", text)
        return text
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Can you please repeat?")
        return listen()
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting to the server.")
        return ""

def get_user_input(prompt):
    speak(prompt)
    return listen()

def save_appointment(name, date, time):
    with open('appointments.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, date, time, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def main():
    speak("Hello! I'm your voice agent to help you schedule a doctor's appointment.")

    name = get_user_input("What is your name?")
    date = get_user_input("On which date would you like to book the appointment?")
    time = get_user_input("What time works best for you?")

    speak(f"Okay {name}, booking your appointment on {date} at {time}.")
    save_appointment(name, date, time)
    speak("Your appointment has been scheduled successfully. Thank you!")

if _name_ == "_main_":
    main()