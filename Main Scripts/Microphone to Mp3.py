import pyaudio
import wave
import threading
import os

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
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
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
command = input("Type 'start' to begin recording: ").strip().lower()
if command == "start":
    start_recording()
    input("Recording... Type 'stop' to end recording: ").strip().lower()
    stop_recording()
