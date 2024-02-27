import flet as ft
import mysql.connector
import pyttsx3
import time
from neuralintents.assistants import BasicAssistant
from vosk import Model, KaldiRecognizer
import sys
import os
import pyaudio
import wave

assistant = BasicAssistant("intents.json")
assistant.fit_model(epochs=20)

engine = pyttsx3.init()

model = Model(f"gigaspeech")
recognizer = KaldiRecognizer(model, 44100)

class Recorder:
    def __init__(self) -> None:

        # constants variables
        self.channel = 1
        self.frequency = 44100
        self.frame_per_rate = 3200
        self.recording_time = 4
        self.format = pyaudio.paInt16
        self.frames = []

        # creating the audio vairable 
        self.audio = pyaudio.PyAudio()

        # creating or initializing the stream
        self.stream = self.audio.open(
            channels=self.channel,
            rate=self.frequency,
            frames_per_buffer=self.frame_per_rate,
            input=True,
            format=self.format
        )

        self.start_recording()

        self.write_audio()

    def start_recording(self):
        for _ in range(0, int(self.frequency/self.frame_per_rate * self.recording_time)):
            voice = self.stream.read(self.frame_per_rate)
            self.frames.append(voice)
        
        # stop the stream 
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def write_audio(self):
        output_file = wave.open(f"voice.wav", "wb")
        output_file.setnchannels(self.channel)
        output_file.setframerate(self.frequency)
        output_file.setsampwidth(self.audio.get_sample_size(self.format))
        output_file.writeframes(b"".join(self.frames))

class Speek:
    def __init__(self, text):
        engine.startLoop()
        engine.say(text=text)

class Black(ft.UserControl):
    def __init__(self) -> None:
        super().__init__()

    def build(self):
        cat = ft.Image(
            src=f"mac.gif",
            width=300,
            height=300,
            border_radius=300
        )
        return ft.Container(content=ft.Row(controls=[
            cat
        ], alignment=ft.MainAxisAlignment.CENTER), margin=100, on_click=lambda e: self.recognition_phase(e))

    def recognition_phase(self, e):
        engine = pyttsx3.init()
        print(f"\n\ncapturing the voice samples...")
        Recorder()
        print("recording completed... (saved in voice.wav file)")

        # converting audio to text
        audio = wave.open("voice.wav", "rb")
        your_text = ""
        while True:
            data = audio.readframes(4096)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                text = recognizer.Result()
                print(f"' {text[14:-3]} '")
                your_text += " " + text[14:-3]
                your_text = str(your_text).strip().lower()

        print(f"\n\nyou said: {your_text}\n\n")

        # commands for windows 
        if "open google" in your_text:
            # code to open goole
            Speek("Starting the Chrome")
            time.sleep(2)
            engine.endLoop()
            os.system("start chrome")
        elif "open microsoft edge" in your_text:
            # code to open edge browser
            Speek("Starting the Microsoft Edge browser")
            time.sleep(3)
            engine.endLoop()
            os.system("start msedge")
        elif "open notepad" in your_text:
            # code to open notepad
            Speek("Starting the Notepad")
            time.sleep(2)
            engine.endLoop()
            os.system("notepad")
        elif "open explorer" in your_text:
            # code to open explorer dialog box
            Speek("Starting the Explorer dialog box")
            time.sleep(2)
            engine.endLoop()
            os.system("explorer")
        elif "open paint" in your_text:
            # code to open paint
            Speek("Starting the Paint Application")
            time.sleep(2)
            engine.endLoop()
            os.system("start chrome")
        elif "open microsoft word" in your_text:
            # code to open microsoft word
            Speek("Starting the Microsoft Word")
            time.sleep(2)
            engine.endLoop()
            os.system("winword")
        elif "open microsoft powerpoint" in your_text:
            # code to open mocrosoft powerpoint
            Speek("Starting the Microsoft Powerpoint")
            time.sleep(2)
            engine.endLoop()
            os.system("powerpnt")
        elif "open microsoft excel" in your_text:
            # code to open microsoft excel
            Speek("Starting the Microsoft Excel")
            time.sleep(2)
            engine.endLoop()
            os.system("start excel")
        elif "open calculator" in your_text:
            # code to open calculator
            Speek("Starting the Calsulator")
            time.sleep(2)
            engine.endLoop()
            os.system("calc")
        elif "stop" in your_text:
            sys.exit(0)
        else:
            response = assistant.process_input(your_text.strip())
            print(response)
            Speek(response)
            time.sleep(3)
            engine.endLoop()
            
class SQL_Manager:
    def __init__(self) -> None:
        pass
    def insertData(self, firstname, lastname, username, password):
        print(firstname, lastname, username, password)
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="brain",
                unix_socket= '/Applications/MAMP/tmp/mysql/mysql.sock',
                raise_on_warnings= True,
                port=8889
            )
            cursor = db.cursor()
            cursor.execute(f"insert into credentials values('{firstname}', '{lastname}', '{username}', '{password}');")
            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            print(f"DB insertData : {e}")
    
    def retriveData(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="brain",
                unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock",
                raise_on_warnings=True,
                port=8889
            )
            cursor=db.cursor()
            cursor.execute("select * from credentials;")
            data = cursor.fetchall()
            cursor.close()
            db.close()
            return data
        except Exception as e:
            print(f"DB retriveData : {e}")

class login_btn(ft.UserControl):
    def __init__(self):
        super().__init__()
    def login_form(self, e):
        self.page.clean()
        self.page.add(Headers(), login())
    def build(self):
        return ft.ElevatedButton("login", on_click=lambda e: self.login_form(e))
    
class register_btn(ft.UserControl):
    def __init__(self):
        super().__init__()
    def register_form(self, e):
        self.page.clean()
        self.page.add(Headers(), register())
    def build(self):
        return  ft.ElevatedButton("register", on_click=lambda e: self.register_form(e))
    
class Headers(ft.UserControl):
    def __init__(self):
        super().__init__()
    def build(self):
        return ft.Container(content=ft.Row(controls=[
            login_btn(), register_btn()
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND))

class login(ft.UserControl):
    def __init__(self):
        super().__init__()
    def login_detials(self, e, username, password):
        data = SQL_Manager().retriveData()
        print(data)
        for i in data:
            if (username in i) and (password in i):
                self.page.clean()
                self.page.add(Headers(), Black())
            else:
                self.page.clean()
                self.page.add(Headers(), login())
    def build(self):
        username = ft.TextField(hint_text="email", autofocus=True)
        password = ft.TextField(hint_text="********", password=True)
        submit = ft.FilledButton(text="login", on_click=lambda e: self.login_detials(e, username.value, password.value))
        login_form = ft.Column(controls=[
            username, password, submit
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=400)
        return ft.Container(content=login_form, alignment=ft.alignment.center, margin=50)
        
class register(ft.UserControl):
    def __init__(self):
        super().__init__()
    def register_detials(self, firstname, lastname, username, password):
        try:
            SQL_Manager().insertData(firstname, lastname, username, password)
            self.page.clean()
            self.page.add(Headers(), login())
        except Exception as e:
            print(f"register register_detials : {e}")
    def build(self):
        firstname = ft.TextField(hint_text="first name", autofocus=True)
        lastname = ft.TextField(hint_text="last name")
        username = ft.TextField(hint_text="enter the email")
        password = ft.TextField(hint_text="********", password=True)
        submit = ft.FilledButton(text="register", on_click=lambda e: self.register_detials(firstname.value, lastname.value, username.value, password.value))
        register_form = ft.Column(controls=[
            firstname, lastname, username, password, submit
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=400)
        return ft.Container(content=register_form, alignment=ft.alignment.center, margin=50)

def main(page: ft.Page):

    page.title = "BRAIN"
    page.window_width = 600
    page.window_height = 600

    page.add(Headers())

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP, port=746, assets_dir="assets")
