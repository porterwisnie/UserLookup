import requests
import summonerData 
from bs4 import BeautifulSoup as bs4
import time
import PIL.Image 
import PIL.ImageTk
from tkinter import *

class Window(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)

        self.master = master
        self.champmastery = IntVar()
        self.init_window()

        

    def init_window(self):

        self.master.title("League Stats Viewer")

        menu = Menu(self.master)

        self.master.config(menu=menu)

   #scrollbar function in the returning text window
        
        scroll = Scrollbar(root)

        self.textArea = Text(root, height=25, width=80,font=('times','13','bold'))

        scroll.pack(side=RIGHT, fill=Y)

        self.textArea.pack(side=RIGHT, fill=Y)
    
        scroll.config(command=self.textArea.yview)
    
        self.textArea.config(yscrollcommand=scroll.set)
    
        
        #label for main search function

        sumLbl = Label(root,text='League of Legends Username Lookup',font=('times','15','bold'))
        
        sumLbl.pack(pady=50)

        #defines the entry field for the lookup username

        self.lookupName = Entry(root,width=20,font=('times','13','bold'))

        self.lookupName.pack(pady=10)

       #search check options

        options = [
                'users stats by champion',

                'basic account info'
                ]

        self.option = StringVar()

        self.option.set(options[0])

        option_menu = OptionMenu(root, self.option, *options)
        
        option_menu.pack(pady=10)
        #champ_option = Checkbutton(root,text='champion mastery info',variable=self.champmastery)

       # champ_option.pack()
        
        Button(root,text='Search',command=self.find_summoner).pack(pady=10)
     
        #toolbar options
        file = Menu(menu)

        file.add_command(label ='About',command=self.about_popup)

        file.add_command(label = 'Exit', command=self.client_exit)

        menu.add_cascade(label='File', menu=file)

        lookup = Menu(menu)
        
        lookup.add_command(label = 'My basic info',command=self.find_summoner_toolbar)

        menu.add_cascade(label='Lookup',menu=lookup)

    def client_exit(self):
            
        exit()
        
    
    def about_popup(self):

        popup = Toplevel()

        message = "League Of Legends Stats Viewer\n  -----------------   \nGithub: porterwisnie\n\nContact me: porterwisniewski@gmail.com"
        
        Label(popup,text=message,wraplength=500,font=('Courier',14,'bold'),fg='black',bg='gray75').pack()
        
        popup.title('About')

        popup.geometry('600x350')

        popup.config(bg='gray75')
    
    def find_summoner(self):
        try:

            self.textArea.delete('1.0',END)

        except:
            pass

        if self.lookupName.get() == '':
               
            self.textArea.insert(END,'Please try entering a username')

        else:

            userId = self.lookupName.get()

            if self.option.get() == 'users stats by champion':

            
                data = summonerData.champ_masteries_by_summoner(userId)

                self.textArea.insert(END,data)


            else:

                self.textArea.insert(END,summonerData.basic_info(userId,'base'))

        self.lookupName.delete(0,END)

    def find_summoner_toolbar(self):

        data = summonerData.basic_info('PorterW','base')
        
        self.textArea.insert(END,data)
        

if __name__=='__main__':

    root = Tk()

    root.geometry("1600x950")

    app = Window(root)

    root.mainloop()
