
import pyaudio
import wave
import time

class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    '''

    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)

class RecordingFile(object):
    def __init__(self, fname, mode, channels, 
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile
       
rec = Recorder(channels=2)
print("RECORDING FOR 5 SECONDS")
with rec.open('speech.wav', 'wb') as recfile2:

    recfile2.start_recording()
    time.sleep(5.0)
    recfile2.stop_recording()

import speech_recognition as sr
r = sr.Recognizer()
words = []


aud = "speech.wav"


with sr.AudioFile(aud) as source:
    
    audio = r.record(source)
    
    
    

data = r.recognize_google(audio)
print(data)

	
import json
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    version = '2017-09-21',
    username = '07b69223-fdca-42d0-b1ae-34136de994a7',
    password = 'CXnyu0n3zOCr',
    url = 'https://gateway.watsonplatform.net/tone-analyzer/api'
)

text =data
    
tone_analysis = tone_analyzer.tone(
    {'text': text},
    'application/json'
).get_result()

data = {'Anger':0, 'Fear':0, 'Joy':0,'Sadness':0, 'Analytical':0, 'Confident':0,'Tentative':0}

for i in tone_analysis['document_tone']['tones']:
        data[i['tone_name']] = i['score']
    
print(data)
        



