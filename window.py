import requests
import summonerData 
from bs4 import BeautifulSoup as bs4
import time
import PIL.Image 
import PIL.ImageTk
from tkinter import *
import champids
import queuetypes

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

        sumLbl = Label(root,text='Stats Lookup\n for League of Legends',font=('times','15','bold'))
        
        sumLbl.pack(pady=50)

        #defines the entry field for the lookup username

        self.lookupName = Entry(root,width=20,font=('times','13','bold'))

        self.lookupName.pack(pady=10)

       #search check options

        options = [
                'users stats by champion',

                'basic account info',

                'match history',

                'account last match indepth',

                'lookup by game id'
                ]
        #defines the game lookup by id search field

        self.lookupGame = Entry(root,width=20,font=('times','13','bold'))

        self.lookupGame.pack(pady=10)


        self.option = StringVar()

        self.option.set(options[0])

        option_menu = OptionMenu(root, self.option, *options)
        
        option_menu.pack(pady=10) 
        
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

        if self.lookupName.get() == '' and len(self.lookupGame.get()) != 10 and str(self.lookupGame.get()).isnum() == False:
               
            self.textArea.insert(END,'Please enter a username or a valid game id')

        else:

            userId = self.lookupName.get()

            if self.option.get() == 'users stats by champion':

            
                data = summonerData.champ_masteries_by_summoner(userId)

                self.textArea.insert(END,data)
            elif self.option.get() == 'match history':

                data = summonerData.recent_matches(userId)

                match_info = ['gameId','lane','champion','queue']

                for match in range(0,len(data)-1):
                    
                    for constant in match_info:
                        if constant == 'champion':
                            self.textArea.insert(END,constant + ': ' + champids.champion_ids[data[match][constant]] + '\n')

                        elif constant == 'queue':
                            try:
                                self.textArea.insert(END, constant+ ': ' + queuetypes.queues[data[match]['queue']]+'\n')
                            except:
                                self.textArea.insert(END,constant + ': ' + str(data[match][constant]) + '\n')
                           
                            self.textArea.insert(END,'----------------\n')

                        else:
                            self.textArea.insert(END,constant + ': ' + str(data[match][constant]) + '\n')
            elif self.option.get() == 'account last match indepth':
                
                data = summonerData.indepth_game(userId)

                self.textArea.insert(END,data)
            elif self.option.get() == 'lookup by game id':

                data = summonerData.game_byId(self.lookupGame.get())

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
