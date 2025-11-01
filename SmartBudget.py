import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"👤 You said: {query}")
    except Exception:
        speak("Sorry, I didn’t get that.")
        return ""
    return query.lower()

def send_email(to, content):
    your_email = "your_email@gmail.com"
    your_password = "your_password"  # <-- use app password if Gmail 2FA
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(your_email, your_password)
        server.sendmail(your_email, to, content)

def tell_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "I told my computer I needed a break, and it said 'No problem — I’ll go to sleep.'",
        "Why did the developer go broke? Because he used up all his cache."
    ]
    speak(random.choice(jokes))

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your personal assistant. How can I help you today?")

def main():
    wish_user()
    while True:
        query = take_command()

        if 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'date' in query:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            speak(f"Today is {date}")

        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak(results)

        elif 'open youtube' in query:
            speak("Opening YouTube.")
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            speak("Opening Google.")
            webbrowser.open("https://google.com")

        elif 'open github' in query:
            speak("Opening GitHub.")
            webbrowser.open("https://github.com")

        elif 'music' in query:
            music_dir = "C:\\Users\\Public\\Music"  # adjust path
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, random.choice(songs)))
            else:
                speak("No music files found.")

        elif 'email' in query:
            try:
                speak("What should I say?")
                content = take_command()
                speak("Who should I send it to?")
                to = input("Enter recipient email: ")
                send_email(to, content)
                speak("Email sent successfully.")
            except Exception as e:
                speak("Sorry, I was unable to send the email.")

        elif 'remember' in query:
            speak("What should I remember?")
            memory = take_command()
            with open('memory.txt', 'w') as f:
                f.write(memory)
            speak("Okay, I will remember that.")

        elif 'do you remember' in query:
            try:
                with open('memory.txt', 'r') as f:
                    speak("You asked me to remember that " + f.read())
            except FileNotFoundError:
                speak("I don’t remember anything yet.")

        elif 'joke' in query:
            tell_joke()

        elif 'stop' in query or 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a great day.")
            break

        else:
            speak("I can’t do that yet, but I’m learning!")
