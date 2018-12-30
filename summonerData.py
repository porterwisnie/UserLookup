import champids

import requests

from bs4 import BeautifulSoup as bs4
global leadUrl

global apiKey
apiKey = 'RGAPI-4c03e04a-098f-4f51-8ca4-74e844355715'

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
    
    return x
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


