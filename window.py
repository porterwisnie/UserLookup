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

        frame = Frame(root,height=300,width=300)

        frame.pack(side=RIGHT,fill=Y)

   #scrollbar function in the returning  frame
        
        scroll = Scrollbar(frame)

        self.textArea = Canvas(frame,width=800,bg='white')

        scroll.pack(side=RIGHT, fill=Y)

            
        scroll.config(command=self.textArea.yview)
    
        self.textArea.config(yscrollcommand=scroll.set)
        
        self.textArea.pack(side=RIGHT, fill=Y)

        
        #label for main search function

        sumLbl = Label(root,text='Stats Lookup\n for League of Legends',font=('times','15','bold'))
        
        sumLbl.pack(pady=50)

        #defines the entry field for the lookup username

        self.lookupName = Entry(root,width=20,font=('times','13','bold'))

        self.lookupName.pack(pady=10)

       #search check options

        options = [
                'Match History',
                'Champion Mastery'
                ]
        #defines the game lookup by id search field

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

        if self.lookupName.get() == '':               
            canvas_id = self.textArea.create_text(0,0,anchor='nw')
            
            self.textArea.itemconfig(canvas_id,text='Please enter a username or a valid game id')

        else:

            userId = self.lookupName.get()

            if self.option.get() == 'Champion Mastery':

            
                data = summonerData.champ_masteries_by_summoner(userId)

            
                canvas_id = self.textArea.create_text(10,10,anchor='nw')

                self.textArea.itemconfig(canvas_id,text=data)
                self.textArea.insert(canvas_id,13,"new ")


            elif self.option.get() == 'Match History':


 
                data = summonerData.recent_matches(userId)

                

                match_info = ['gameId','lane','champion','queue']
                recent_match_overview = []
                for match in range(0,len(data)-1):
                    match_dict = {}
                    for constant in match_info:
                        if constant == 'champion':
                            match_dict['champion'] = champids.champion_ids[data[match]['champion']]
                        elif constant == 'queue':
                    
                            match_dict['queue'] = queuetypes.queues[data[match]['queue']]
                           
                        

                        else:
                            match_dict[constant] = data[match][constant]
                    recent_match_overview.append(dict(match_dict)) 

                game_list = []
                  
                for game in recent_match_overview:

                    game_info = summonerData.game_byId(game['gameId'])

                    game_list.append(game_info)


                    '''
                    before this sleep timer the objective is to have code that creates a replicating rectangle with:
                        
                        Username and K/D/A
                        ?intergrate champion pics to show who they were playing?
                        
                    then have a bar across the bottom of these stats with button/buttons for more info

                    ---------------------------------------------------------------
                    |                      |"more info"|                          |
                    ---------------------------------------------------------------

                    something like this to have at the bottom of each in the canvas on the right

                    have the button make a popup that gives advanced/more indepth stats

                    ?graphing options with variable x and y axis for comparison?

                    ***IMPORTANT***

                    make it so ALL of the info is still easily accesible for data interpertation in the popup

                    basically so i can use everything later on if I need to

                    _________________________________________________________________________

                    
                    '''

                    time.sleep(1)

                
                print(game_list)

            

    def find_summoner_toolbar(self):

        data = summonerData.basic_info('PorterW','base')
        
        self.textArea.insert(END,data)
        

if __name__=='__main__':

    root = Tk()

    root.geometry("1600x950")

    app = Window(root)

    root.mainloop()
