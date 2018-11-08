import os


#os.system("cd")
#os.system("cd Desktop/performance_rnn")
os.system("cd music")
os.system("find . -type f -name '*.wav' -exec rm {} +")
os.system("cd ..")
os.system("cd midi")
os.system("find . -type f -name '*.mid' -exec rm {} +")
os.system("cd ..")
os.system("find . -type f -name '*.wav' -exec rm {} +")