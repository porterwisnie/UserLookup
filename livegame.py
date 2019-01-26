import requests
import json
from bs4 import BeautifulSoup as bs4
import champids
import queuetypes
import time
from summonerData import apiKey
def live_game(summId):

    leadUrl = 'lol/summoner/v4/summoners/by-name'
    #first request finds the summoner Id number for the name given in the search
    response = requests.get('https://na1.api.riotgames.com/{}/{}?api_key={}'.format(leadUrl,summId,apiKey))

    soup = bs4(response.text,'lxml')

    x = soup.get_text()

    js_response = json.loads(x)

    #summoner Id is equal to the number value given by riot games here 
    summId = js_response['id']


    #searches for live games with player matching encryted summoner id
    live_response = requests.get('https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{}?api_key={}'.format(summId,apiKey))

    soup = bs4(live_response.text,'lxml')

    js_response = json.loads(soup.get_text())
    print(js_response)
    return js_response

