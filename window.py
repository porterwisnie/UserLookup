import requests
import summonerData 
from bs4 import BeautifulSoup as bs4
import time
import PIL.Image 
import PIL.ImageTk
from tkinter import *
import champids
import queuetypes
import os
from sys import platform

class Window(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)

        self.master = master
        self.champmastery = IntVar()
        self.init_window()
        self.game_list = []
        #used by the find_summoner method and the more_stats function for identifying which game was clicked
        self.gamenum = 0
        self.itemImages = []
        
        master.bind('<Return>',self.find_summoner_enter)


    def init_window(self):

        self.master.title("League Stats Viewer")

        menu = Menu(self.master)

        self.master.config(menu=menu)

        frame = Frame(root,height=300,width=300)

        frame.pack(side=RIGHT,fill=Y)
   #scrollbar function in the returning  frame
        
        scroll = Scrollbar(frame)

        self.textArea = Canvas(frame,width=1000,bg='white')

        scroll.pack(side=RIGHT, fill=Y)

            
        scroll.config(command=self.textArea.yview)
    
        self.textArea.config(yscrollcommand=scroll.set)

        self.textArea.config(yscrollincrement='5')
        
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
        tip = Label(root,text='tip: click on game to see more info',font=('times','13','bold'))
        
        tip.pack(pady=50)
    def client_exit(self):
            
        exit()
        
    
    def about_popup(self):

        popup = Toplevel()

        message = "League Of Legends Stats Viewer\n  -----------------   \nGithub: porterwisnie\n\nContact me: porterwisniewski@gmail.com"
        
        Label(popup,text=message,wraplength=500,font=('Courier',14,'bold'),fg='black',bg='gray75').pack()
        
        popup.title('About')

        popup.geometry('600x350')

        popup.config(bg='gray75')


    def find_summoner_enter(self,event=None):
        
        self.find_summoner()
   
    
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

                
                  
                for game in recent_match_overview:

                    self.game_list.append(summonerData.game_byId(game['gameId']))
                

                xpos = 50

                ypos = 10

                team2ypos = 10

                fillcolor = 'red'

                for game in self.game_list:

                    
                
                    identity = game['participantIdentities'] 

                    per_game_area = self.textArea.create_rectangle(0,ypos-10,1000,ypos+400,fill=fillcolor,tags=str(self.gamenum))

                    self.gamenum += 1

                    for participant in range(0,10):

                        indiv_data = game['participants'][participant] 

                        if self.lookupName.get() == identity[participant]['player']['summonerName'] and indiv_data['stats']['win'] == True:

                            self.textArea.itemconfig(per_game_area,fill='green')
                         
                        if participant == 0:

                            self.textArea.create_text((50,ypos),text='Winning team',anchor='w')

                            self.textArea.create_text((550,team2ypos),text='Losing team',anchor='w')

                            ypos += 30

                            team2ypos += 30

                        if indiv_data['stats']['win'] == False:

                            xpos = 550

                            self.textArea.create_text((xpos,team2ypos),text=str(identity[participant]['player']['summonerName'])+'\n   '+str(champids.champion_ids[indiv_data['championId']])+'   '+str(indiv_data['stats']['kills'])+'/'+str(indiv_data['stats']['deaths'])+'/'+str(indiv_data['stats']['assists']),anchor='w')
                            
                            team2ypos +=40
                        else:
                            xpos = 50
     
                            self.textArea.create_text((xpos,ypos),text=str(identity[participant]['player']['summonerName'])+'\n   '+str(champids.champion_ids[indiv_data['championId']])+'   '+str(indiv_data['stats']['kills'])+'/'+str(indiv_data['stats']['deaths'])+'/'+str(indiv_data['stats']['assists']),anchor='w')
            
                            ypos += 40

                        if participant == 9:            
                           
                            self.textArea.tag_bind(per_game_area,'<Button-1>',self.ongame_click)







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

    def ongame_click(self,other): 

        x = int(self.textArea.find_withtag("current")[0])
  
        self.gamenum = (x-1)//13
        
        self.more_stats()
    def more_stats(self):

        ## Notes for next time
        # Find a way to track which game is clicked on 
        #fix formatting with the popup after only the selected game is shown
        popup = Toplevel()

        message = "Game Info"
        
        Label(popup,text=message,wraplength=500,font=('Courier',14,'bold'),fg='black',bg='gray75').pack()
        
        popup.title('More Stats')

        popup.geometry('1000x700')

        popup.config(bg='gray75') 

        
        #####
        pframe = Frame(popup,height=800,width=700)

        pframe.pack()

        scroll = Scrollbar(pframe)

        ptextArea = Canvas(pframe,width=1000,bg='white',height=600)

        scroll.pack(side=RIGHT, fill=Y)

            
        scroll.config(command=ptextArea.yview)
    
        ptextArea.config(yscrollcommand=scroll.set)

        ptextArea.config(yscrollincrement='5')
        
        ptextArea.pack()
        #####
        ypos = 40

        xpos = 40

        team2ypos = 300

        game = self.game_list[self.gamenum]
                
        identity = game['participantIdentities'] 

        for participant in range(0,10):

            indiv_data = game['participants'][participant] 

            player_highlight = 'white'

            itemxpos = 525

            if self.lookupName.get() == identity[participant]['player']['summonerName'] and indiv_data['stats']['win'] == True:
                #use this if statement to match who the lookup was searching for
                player_highlight = 'gray'
             
            if participant == 0: 

                ptextArea.create_text((xpos,ypos),text='Winning team',anchor='w')
                #labels for the columns of data
                ptextArea.create_text((xpos+300,ypos),text='Gold\nSpent|Earned',anchor='w')
                
                ptextArea.create_text((xpos+800,ypos),text='Vision\nScore',anchor='w')

                ptextArea.create_text((xpos+550,ypos),text='Items',anchor='w')

                ypos += 40

                ptextArea.create_text((xpos,team2ypos),text='Losing team',anchor='w')

                team2ypos+=40

            if indiv_data['stats']['win'] == False:

                ptextArea.create_text((xpos,team2ypos),text=(str(identity[participant]['player']['summonerName']))+'\n   '+str(champids.champion_ids[indiv_data['championId']])+'   '+str(indiv_data['stats']['kills'])+'/'+str(indiv_data['stats']['deaths'])+'/'+str(indiv_data['stats']['assists']),anchor='w')

                ptextArea.create_text((xpos+800,team2ypos),text=str(indiv_data['stats']['visionScore']))
                
                ptextArea.create_text((xpos+300,team2ypos),text=str(indiv_data['stats']['goldSpent'])+'|'+str(indiv_data['stats']['goldEarned']),anchor='w')

                item_list = []

                for num in range(0,7,1): 
                    itemId = indiv_data['stats']['item{}'.format(str(num))]

                    if itemId > 0:
                    
                
                        image_string = summonerData.getitem(itemId)

                        item_list.append([itemxpos,team2ypos,image_string])

                        #image = PhotoImage(file=image_string)
                    
                        #ptextArea.create_image((itemxpos,team2ypos),image=image,anchor='w')

                        itemxpos+=30

                        
                for item in item_list:
                    
                    item_image = PIL.Image.open(item[2])

                    item_image = item_image.resize((30,30),PIL.Image.ANTIALIAS)

                    itemimg = PIL.ImageTk.PhotoImage(item_image)

                    ptextArea.create_image((item[0],item[1]),image = itemimg,anchor='w')

                    self.itemImages.append(itemimg)
 
                team2ypos +=40
            else:

                ptextArea.create_text((xpos,ypos),text=(str(identity[participant]['player']['summonerName']))+'\n   '+str(champids.champion_ids[indiv_data['championId']])+'   '+str(indiv_data['stats']['kills'])+'/'+str(indiv_data['stats']['deaths'])+'/'+str(indiv_data['stats']['assists']),anchor='w')

                ptextArea.create_text((xpos+800,ypos),text=str(indiv_data['stats']['visionScore']),anchor='w')

                ptextArea.create_text((xpos+300,ypos),text=str(indiv_data['stats']['goldSpent'])+'|'+str(indiv_data['stats']['goldEarned']),anchor='w')

                item_list = []

                for num in range(0,7,1): 
                    itemId = indiv_data['stats']['item{}'.format(str(num))]

                    if itemId > 0:
                    
                
                        image_string = summonerData.getitem(itemId)

                        item_list.append([itemxpos,ypos,image_string])

                        #image = PhotoImage(file=image_string)
                    
                        #ptextArea.create_image((itemxpos,team2ypos),image=image,anchor='w')

                        itemxpos+=30

                            
                    for item in item_list:
                        
                        item_image = PIL.Image.open(item[2])

                        item_image = item_image.resize((30,30),PIL.Image.ANTIALIAS)

                        itemimg =  PIL.ImageTk.PhotoImage(item_image,width=100,height=100)

                        

                        ptextArea.create_image((item[0],item[1]),image = itemimg,anchor='w')

                        self.itemImages.append(itemimg)
     
                        

                ypos +=40
    


            

    def find_summoner_toolbar(self):

        data = summonerData.basic_info('PorterW','base')
        
        self.textArea.insert(END,data)
        

if __name__=='__main__':

    root = Tk()

    root.geometry("1600x950")
    if platform == 'Windows':

        root.iconbitmap(os.getcwd()+'/3089.ico')

    else:
        
        img = Image("photo",file=os.getcwd()+'/items/3089.png')
        root.tk.call('wm','iconphoto',root._w,img)

    app = Window(root)

    root.mainloop()
