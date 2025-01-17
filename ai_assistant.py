import sys
import threading
import tkinter as tk
import speech_recognition
import pyttsx3 as tts
from neuralintents import BasicAssistant


class Assistant:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)

        self.assistant = BasicAssistant("intents.json")

        self.root = tk.Tk()
        self.root.title("AI Assistant")
        self.root.geometry("400x400")
        self.root.configure(bg="white")
        self.label = tk.Label(text="ROBOT", font=("Arial", 20), bg="white", fg="black")
        self.label.pack(pady=20)

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()

    def create_file(self, file_name):
        with open(file_name, "w") as file:
            file.write("HELLO WORLD")

    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    print("Listening...")
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    if "hey robot" in text:
                        self.label.config(fg="red")
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        if text == "stop":
                            self.speaker.say("Goodbye")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit()
                        else:
                            if text is not None:
                                response = self.assistant.request(text)
                                if response is not None:
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()
                                self.label.config(fg="black")
            except:
                self.label.config(fg="black")
                continue


Assistant()
