import pyaudio
import wave
import threading
import os

from google.cloud import speech
import google.generativeai as genai

from fpdf import FPDF

FORMAT = pyaudio.paInt16  
CHANNELS = 1 
RATE = 44100  
CHUNK = 1024  

audio = pyaudio.PyAudio()
frames = []  
recording = False  

def get_next_filename():
    i = 1
    while True:
        filename = f"op{i}.wav"
        if not os.path.exists(filename):
            return filename
        i += 1

def start_recording():
    global recording
    recording = True
    frames.clear()
    print("Recording started...")

    def record():
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        while recording:
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()

    threading.Thread(target=record).start()

def stop_recording():
    global recording
    recording = False
    print("Recording stopped.")
    file_name = get_next_filename()
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Recording saved as {file_name}")
    return file_name

def speech_to_text(file_name):
    client = speech.SpeechClient.from_service_account_file('key.json')
    with open(file_name, "rb") as f:
        mp3_data = f.read()

    audio = speech.RecognitionAudio(content=mp3_data)
    config = speech.RecognitionConfig(
        sample_rate_hertz=44100,
        enable_automatic_punctuation=True,
        language_code="en-US"  
    )

    response = client.recognize(config=config, audio=audio)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
    return transcript

def clean_text_with_gemini(response_text):
    api_key = 'AIzaSyDHs6a-KYnyF2Eyfw11QEscDfTAcqU-aWM'
    genai.configure(api_key=api_key)
    
    prompt = (
        "Clean this text by removing all irrelevant content such as announcements, distractions, "
        "and non-teaching parts. Only keep the main teaching material. If there are grammar mistakes, correct them."
        "\n\n" + response_text
    )
    model = genai.GenerativeModel('gemini-pro')
    cleaned_response = model.generate_content(prompt)
    
    return cleaned_response.text
def save_to_pdf(cleaned_response, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    response_lines = cleaned_response.split('\n')
    for line in response_lines:
        pdf.multi_cell(0, 10, txt=line)
    
    pdf_file_name = file_name.replace('.wav', '_cleaned.pdf')
    pdf.output(pdf_file_name)
    print(f"Cleaned response saved as {pdf_file_name}")

command = input("Type 'start' to begin : ").strip().lower()
if command == "start":
    start_recording()
    input("Recording... Type 'stop' to end : ").strip().lower()
    file_name = stop_recording()

    response_text = speech_to_text(file_name)
    print(f"Transcribed Response:\n{response_text}")
    cleaned_response = clean_text_with_gemini(response_text)
    print(f"Cleaned Response:\n{cleaned_response}")

    save_to_pdf(cleaned_response, file_name)
