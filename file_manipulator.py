import logging
import time

import PyPDF2
import pyttsx3
import pywhatkit

BLUE = (0, 0, 255)


class TextManipulator:
    def __init__(self, file_name):
        self.speaker = pyttsx3.init()
        self.file_name = file_name
        self.text = ""
        self.pdfReader = None
        self.file_extension = self.file_name.split(".")[-1]

    def read_file(self):
        if self.file_extension.endswith("pdf"):
            self.text = ""
            self.pdfReader = PyPDF2.PdfFileReader(open(self.file_name, 'rb'))
            for page_num in range(self.pdfReader.numPages):
                self.text += self.pdfReader.getPage(page_num).extractText()
        elif self.file_extension.endswith(('txt', "text")):
            with open(self.file_name) as text_file:
                self.text = text_file.read()
        else:
            logging.error("File type not supported !")

    def read_audio(self, save_audio=False,  audio_name=None):
        if not self.text:
            self.read_file()
        self.speaker.say(self.text)
        self.speaker.runAndWait()
        self.speaker.stop()
        if save_audio:
            self.save_audio(audio_name)

    def save_audio(self, audio_name="./audio.mp3"):
        if not self.text:
            self.read_file()
        self.speaker.save_to_file(self.text, audio_name)
        self.speaker.stop()

    def create_hand_writing(self, destination_file="hand_writing.png", rgb_color=BLUE):
        """Creates a .png file by default"""
        pywhatkit.text_to_handwriting(self.text, save_to=destination_file, rgb=rgb_color)


if __name__ == '__main__':
    text_manipulator = TextManipulator(file_name="test_file.txt")
    text_manipulator.read_file()
    text_manipulator.read_audio()
    text_manipulator.save_audio()
    text_manipulator.create_hand_writing()

