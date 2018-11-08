
# coding: utf-8

# In[ ]:


import speech_recognition as sr
r = sr.Recognizer()
words = []

with sr.Microphone() as source:
    print("SAY SOMETHING")
    
    audio = r.listen(source)
    print("TIME OVER")
    
    #rec.save("test.wav")

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
        




# In[103]:





# In[90]:


print(tonename)
print(score)

