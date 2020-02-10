import json
import csv
import requests

#api_key = "RGAPI-90016878-a351-48cf-a859-845d0deb8ff1"

def getQueryRanked(league, division, key):
    URL = 'https://na1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/'+league+'/'+division+'?page=1&api_key='+RGAPI-a38cd283-be44-4395-9d5a-fe17e4fd35a7+'
    response = response.text(URL)
    r = json.loads(response)
    c = csv.writer(open("bar-data.csv", "w"), lineterminator='\n')

    c.writerow(['wins', 'loss'])
    for x in range(len(r)):
        c.writerow([r[x]['wins'], r[x]['losses']])