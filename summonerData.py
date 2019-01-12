import champids

import requests

import json

import os

from bs4 import BeautifulSoup as bs4

from PIL import Image
global leadUrl

global apiKey
apiKey = 'RGAPI-fa5419f0-1aa5-4a81-8153-c1948f63bed4'

global summId


def is_ascii(string):
        return all(ord(c) < 128 for c in string)

def sumLookup(summId,lookup):


    if summId == is_ascii(summId):
        return 'please enter valid characters'

    else:

        if lookup == 'base':

            leadUrl = 'lol/summoner/v3/summoners/by-name'

            summId = 'PorterW'

            return [summId,leadUrl]

        elif lookup == 'champ masters':

            leadUrl = 'lol/summoner/v3/summoners/by-name'
            #first request finds the summoner Id number for the name given in the search
            response = requests.get('https://na1.api.riotgames.com/{}/{}?api_key={}'.format(leadUrl,summId,apiKey))

            soup = bs4(response.text,'lxml')

            x = soup.get_text()
        
            comma_seperated = x.split(',')
    
            dictionary = {}
    
            for item in comma_seperated:

                splitvalue = item.split(':')

                dictionary[splitvalue[0]] = splitvalue[1]
            #summoner Id is equal to the number value given by riot games here 
            summId = dictionary['{"id"']

            leadUrl = 'lol/champion-mastery/v3/champion-masteries/by-summoner'
            return [summId,leadUrl]
        elif lookup == 'recent matches':

            leadUrl = 'lol/summoner/v3/summoners/by-name'
            #first request finds the summoner Id number for the name given in the search
            response = requests.get('https://na1.api.riotgames.com/{}/{}?api_key={}'.format(leadUrl,summId,apiKey))

            soup = bs4(response.text,'lxml')

            x = soup.get_text()
        
            comma_seperated = x.split(',')
    
            dictionary = {}
    
            for item in comma_seperated:

                splitvalue = item.split(':')

                dictionary[splitvalue[0]] = splitvalue[1]
            #summoner Id is equal to the number value given by riot games here 
            
            summId = dictionary['\"accountId\"']

            return summId
            
#below is the request and basic processing for the terms defined above
def single_response_as_dict(leadUrl,summId,apiKey):

    response = requests.get('https://na1.api.riotgames.com/{}/{}?api_key={}'.format(leadUrl,summId,apiKey))

    soup = bs4(response.text,'lxml')

    x = soup.get_text()
        
    comma_seperated = x.split(',')
    
    dictionary = {}
    
    for item in comma_seperated:

        splitvalue = item.split(':')

        dictionary[splitvalue[0]] = splitvalue[1]
    return dictionary
def basic_info(summId,lookup):

    response = sumLookup(summId,lookup)

    summId = response[0]

    leadUrl = response[1]
    
    x = single_response_as_dict(leadUrl,summId,apiKey)

def recent_matches(summId):
    summId = sumLookup(summId,'recent matches')

    leadUrl = 'lol/match/v3/matchlists/by-account'

    response = requests.get('https://na1.api.riotgames.com/{}/{}?endIndex=20&api_key={}'.format(leadUrl,summId,apiKey))
   
    soup = bs4(response.text,'lxml')

    x = soup.get_text()

    json_response = json.loads(x)

    return json_response['matches'] 

def indepth_game(summId):
    json_response = recent_matches(summId) 

    game_id = json_response[0]['gameId']

    leadUrl = 'lol/match/v3/matches'

    response = requests.get('https://na1.api.riotgames.com/{}/{}?api_key={}'.format(leadUrl,game_id,apiKey))

    soup = bs4(response.text,'lxml')

    x = soup.get_text()

    data = json.loads(x)

    return data

def game_byId(gameId):

    leadUrl = 'lol/match/v3/matches'

    response = requests.get('https://na1.api.riotgames.com/{}/{}?api_key={}'.format(leadUrl,gameId,apiKey))

    soup = bs4(response.text,'lxml')

    x = soup.get_text()

    data = json.loads(x)

    return data


    
def champ_masteries_by_summoner(summId):
    #requests the info 
    response = sumLookup(summId,'champ masters')

    summId = response[0]

    leadUrl = response[1]

    response = requests.get('https://na1.api.riotgames.com/{}/{}?api_key={}'.format(leadUrl,summId,apiKey))

    soup = bs4(response.text,'lxml')

    x = soup.get_text()
        
    comma_seperated = x.split(',')

    dictionarylist = []

    count = 1
    #basic attributes of each lookup 
    attributes = ['player id','champion id', 'champion level','champion points','last play time','champion points since last level','champ points to next level','chest granted']
    splitdict = dict()
    for item in comma_seperated:
    
        if count % 9 ==0:
            dictionarylist.append(splitdict.copy())
            
            count = 1
            
        else:
            splitvalue = item.split(':')

            splitdict.update({attributes[count-1]:splitvalue[1]})

            count +=1

    infoList = []
    for obj in dictionarylist:

        for k,v in obj.items():
            if k == 'champion id':
                v = champids.champion_ids[int(obj[k])]
            if k != 'player id' and k != 'chest granted':
                infoList.append('{}:{}\n'.format(k,v))
            elif k == 'chest granted':
                infoList.append('{}:{}\n-----------------------\n'.format(k,v))
     
    return infoList

#gets image for each item id

def getitem(item):

#returns path to the image of item

    pwd = os.getcwd()
    if os.path.isfile('{}/items/{}.png'.format(pwd,item)) == False:
        response = requests.get('http://ddragon.leagueoflegends.com/cdn/9.1.1/img/item/{}.png'.format(item))

        time.sleep(.75)

        if response.status_code == 200:
            with open('{}/items/{}.png'.format(pwd,item),'wb') as f:
                f.write(response.content)
    return "{}/items/{}.png".format(pwd,item)
    
        
            
                
            

