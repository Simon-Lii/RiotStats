import json
import csv
import requests
import timeit

#api_key = "RGAPI-90016878-a351-48cf-a859-845d0deb8ff1"

def getQueryLeagueExp(league, division, api_key):
    oldData = []
    pageNum = 1
    while True:
        URL = 'https://na1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/'+league+'/'+division+'?page='+str(pageNum)+'&api_key='+api_key
        r = requests.get(URL)
        r = r.json()
        if r == []:
            break
        oldData = r + oldData
        pageNum+=1
    c = csv.writer(open("csv/"+league+""+division+".csv", "w"), lineterminator='\n')
    r = oldData
    c.writerow(['wins', 'loss'])
    for x in range(len(r)):
        c.writerow([r[x]['wins'], r[x]['losses']])

API_KEY = 'RGAPI-8b34f9fd-4b18-477c-903e-1b2520a85f0c'
start = timeit.default_timer()
getQueryLeagueExp('DIAMOND', 'III', API_KEY)
stop = timeit.default_timer()
print('Time: ', stop - start) 
