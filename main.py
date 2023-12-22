import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
from pydub import AudioSegment
import threading
import webbrowser
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

chosen_file = ""  # Global variable to store the chosen file name

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('opinion_lexicon')

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file)
    audio.export("transcript.wav", format="wav")

    with sr.AudioFile("transcript.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

    return text

def get_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    return scores

def get_pos_tags(text):
    tokens = word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    return pos_tags

def open_file():
    global chosen_file
    chosen_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if chosen_file:
        result_text.delete(1.0, tk.END)  # Clear previous text
        transcribed_text = transcribe_audio(chosen_file)
        result_text.insert(tk.END, transcribed_text)
        show_message(f"Text is recorded from: {chosen_file}")
        analyze_text(transcribed_text)

def start_recording():
    def record_audio():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio_data = recognizer.record(source, duration=5)  # Record for a maximum of 5 seconds

        audio = AudioSegment(audio_data.frame_data, frame_rate=audio_data.sample_rate, sample_width=audio_data.sample_width, channels=1)
        audio.export("recorded.wav", format="wav")  # Export recorded audio

        transcribed_text = transcribe_audio("recorded.wav")
        result_text.delete(1.0, tk.END)  # Clear previous text
        result_text.insert(tk.END, transcribed_text)
        show_message("Audio recorded and transcribed.")
        analyze_text(transcribed_text)

    threading.Thread(target=record_audio).start()

def analyze_text(text):
    sentiment = get_sentiment(text)
    pos_tags = get_pos_tags(text)

    positive_words = sum(1 for _, tag in pos_tags if tag == 'JJ' and tag == 'RB' and tag == 'VBG' and tag == 'UH')
    negative_words = sum(1 for _, tag in pos_tags if tag == 'NEG' and tag == 'JJ')

    show_message(f"Sentiment Scores: {sentiment}")
    show_message(f"Number of positive words: {positive_words}")
    show_message(f"Number of negative words: {negative_words}")

def open_resume():
    webbrowser.open("https://drive.google.com/file/d/1bfnVKNMw7j8aIFF7s0SEswzcPTagolQQ/view?usp=drive_link")

def show_message(msg):
    message_label.config(text=msg)

root = tk.Tk()
root.title("Audio to Text Converter")

# UI Layout
label_name = tk.Label(root, text="Name: Yash Rawal", font=("Arial", 12, "bold"))
label_name.pack()

label_university = tk.Label(root, text="Parul University", font=("Arial", 12, "italic"))
label_university.pack()

label_resume = tk.Label(root, text="Link to Resume", font=("Arial", 12), fg="blue", cursor="hand2")
label_resume.pack()
label_resume.bind("<Button-1>", lambda e: open_resume())

label_file = tk.Label(root, text="Select an audio file:")
label_file.pack()

button_browse = tk.Button(root, text="Browse", command=open_file)
button_browse.pack()

button_record = tk.Button(root, text="Record", command=start_recording)
button_record.pack()

label_transcribed = tk.Label(root, text="Transcribed Text:")
label_transcribed.pack()

result_text = tk.Text(root, height=10, width=50)
result_text.pack()

message_label = tk.Label(root, text="")
message_label.pack()

root.mainloop()
