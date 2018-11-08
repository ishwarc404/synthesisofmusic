import pandas as pd
from subprocess import call
import os
import re
#[2, 0, 1, 0, 3, 1, 0, 1, 0, 1, 0, 1] =>.5 happy
#[2, 0, 0, 0, 1, 1, 0, 2, 0, 1, 0, 1] => .7 happy
#[2, 0, 0, 0, 1, 0, 0, 2, 0, 1, 0, 0] => .8 happy
#[2, 0, 0, 0, 1, 1, 0, 4, 0, 1, 0, 0] => 1 happy
#[2, 0, 1, 1,0 , 1, 0, 2, 0, 1, 1, 0] =>0.6 sad
#[2, 1, 1, 1, 0 , 1, 0, 2, 1, 0, 1, 0] =>0.6 sad
#[2, 1, 1, 1, 0 , 1, 0, 2, 1, 0, 1, 0] => 0.7-8 sad  (danger)

import pyaudio
import wave
import time
import json
from watson_developer_cloud import ToneAnalyzerV3
n_sec = 7
beam_size = 1
primer_melody = str([57, 64, 67,76,52])

os.system("cd music")
print(os.system("ls -l"))
os.system("rm *.wav")
os.system("cd ..")
os.system("cd midi")
os.system("rm *.mid")
os.system("cd ..")
os.system("rm long.wav")
print("LMAO")

class Recorder(object):
    '''#A recorder class for recording audio to a WAV file.
    #Records in mono by default.
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
with open('./txts/speech.txt', 'r') as content_file:
    content = content_file.read()
print(content)
data1=content.replace('.','\n').replace(',','\n').split('\n')
print(data1)
tone_analyzer = ToneAnalyzerV3(
    version = '2017-09-21',
    username = '07b69223-fdca-42d0-b1ae-34136de994a7',
    password = 'CXnyu0n3zOCr',
    url = 'https://gateway.watsonplatform.net/tone-analyzer/api'
)
datalist = []
cnt=0
for k in data1:
    if k !='':
        cnt+=1
        datadic = {'Anger':0, 'Fear':0, 'Joy':0,'Sadness':0, 'Analytical':0, 'Confident':0,'Tentative':0}

        text = k
        tone_analysis = tone_analyzer.tone(
            {'text': text},
            'application/json'
        ).get_result()

        for i in tone_analysis['document_tone']['tones']:
            datadic[i['tone_name']] = i['score']

        datalist.append(datadic)

with open('./txts/speech.txt', 'w+') as the_file:
    for i in data1:
        if (i !=' '):
            the_file.write(i)
            the_file.write("\n")

        

    



for data in datalist:

    if data['Sadness'] < 0.5:
        hist = [2, 0, 1, 1, 0, 1, 0, 2, 0, 1, 1, 0]
    elif data['Sadness'] < 0.6:
        n_sec = 5
        hist = [2, 1, 1, 1, 0, 1, 0, 2, 1, 0, 1, 0]
    else:
        n_sec = 5
        hist=[2, 1, 1, 1, 0, 1, 0, 2, 1, 0, 1, 0]

    if data['Joy'] < 0.5:

        hist = [2, 0, 1, 0, 3, 1, 0, 1, 0, 1, 0, 1]
    elif data['Joy']  < 0.6 or data['Confident']  < 0.6:
        hist = [2, 0, 0, 0, 1, 1, 0, 2, 0, 1, 0, 1]
    elif data['Joy']  < 0.7 or data['Confident']  < 0.7:
        hist = [2, 0, 0, 0, 1, 0, 0, 2, 0, 1, 0, 0]
    else:
        hist = [2, 0, 0, 0, 1, 1, 0, 4, 0, 1, 0, 0]

    print('performance_rnn_generate --config=\'multiconditioned_performance_with_dynamics\' --bundle_file=multiconditioned_performance_with_dynamics.mag --output_dir=./midi --num_outputs=1 --num_steps=6000 --temperature=0.95 --beam_size='+str(beam_size)+' --primer_melody1=\"' + str(primer_melody) + '\" --notes_per_second='+str(n_sec)+'  --pitch_class_histogram=\"' +
              str(hist) + '\"')

    hist = str(hist)
    os.system('performance_rnn_generate --config=\'multiconditioned_performance_with_dynamics\' --bundle_file=multiconditioned_performance_with_dynamics.mag --output_dir=./midi --num_outputs=1 --num_steps=1000 --temperature=0.95 --beam_size='+str(beam_size)+' --primer_pitches=\"' + primer_melody + '\" --notes_per_second='+str(n_sec)+'  --pitch_class_histogram=\"' +
              hist + '\"')

from midi2audio import FluidSynth

count  = cnt
wavfiles = []
fs = FluidSynth()
for filename in os.listdir('./midi'):
    filename = os.fsdecode(filename)
    if filename.endswith(".mid"): 
        print('midi2audio ./midi/'+filename+' ./music/'+filename[:-4]+'.wav')
        os.system('midi2audio ./midi/'+filename+' ./music/'+filename[:-4]+'.wav')
print('wavs CREATED')
command = "sox"

for filename in os.listdir('./music'):
    if filename.endswith(".wav"):
        command = command + " "+ "./music/"+filename

command  = command + " -t wav "+ "long.wav"
print(command)
os.system(command)


print(".wav FILE CREATED")    
