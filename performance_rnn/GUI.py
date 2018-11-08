from tkinter import * 
import os
from midi2audio import FluidSynth
from pygame import mixer
import time



window = Tk()
window.geometry('600x600')
window.title("STORY BOARD")
textt = StringVar()
count = 0



 

def clicked():
    datalist = []
    
    textt = text.get('1.0',END)
    datalist=textt.replace('.','\n').replace(',','\n').split('\n')
    #datalist = datalist.split('\n')


    count = len(datalist)
    #print(textt)
    audioplay = Tk()
    audioplay.geometry('600x600')
    i = 0;
    with open('./txts/speech.txt', 'w+') as the_file:
        for i in datalist:
            
                the_file.write(i)
                the_file.write("\n")
    print("File contents received");
     
    os.system("python3 music_para.py")
    

     #neeed to play the long.wav file now
     #initializing pygame
    def playmusic():
        
        time.sleep(2.0)
        mixer.init()
        mixer.music.load("long.wav")
        mixer.music.play()
        for i in datalist :
            print(i)
            label = Label(window,text ="Script")
            label.grid(column=1, row=4)
            label.config(text=i)
            label.after(10000)
            time.sleep(10.0)
            label.destroy()

        




        



   


    b = Button(audioplay, text="PLAY MUSIC", command=playmusic)

    b.grid(column=2, row=3)


        


   
   



text = Text(window)
text.grid(column=1, row=0)
btn = Button(window, text="GENERATE A TUNE", command=clicked,height=3, width=15)
btn.grid(column=1, row=2,)


window.mainloop()

