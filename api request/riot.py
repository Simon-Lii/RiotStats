import json
import csv
import requests
import timeit

#api_key = "RGAPI-90016878-a351-48cf-a859-845d0deb8ff1"

def getQueryLeagueExp(league, division, api_key):
    oldData = []
    pageNum = 1
    CONST_RATE_LIMIT_TEST = 100
    while True:
        URL = 'https://na1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/'+league+'/'+division+'?page='+str(pageNum)+'&api_key='+api_key
        r = requests.get(URL)
        r = r.json()
        if r == [] or pageNum == CONST_RATE_LIMIT_TEST:
            break
        oldData = r + oldData
        #print(pageNum)
        pageNum+=1
    c = csv.writer(open("csv/"+league+""+division+".csv", "w"), lineterminator='\n')
    r = oldData
    c.writerow(['wins', 'loss'])
    for x in range(len(r)):
        c.writerow([r[x]['wins'], r[x]['losses']])

API_KEY = 'RGAPI-0615732a-761c-45c1-9134-9c7e203ab047'
#start = timeit.default_timer()
#getQueryLeagueExp('DIAMOND', 'I', API_KEY)
#stop = timeit.default_timer()
#print('Time: ', stop - start) 

def getAccountId(summonerName, API_KEY):
    # replace all white space in summonerName to %20
    # it is safe to mutate summonerName because summonerName is not a pointer! 
    # Memory is taken from the stack.
    summonerName = summonerName.replace(" ", "%20")
    #print(summonerName)
    URL = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+summonerName+'?api_key='+API_KEY
    r = requests.get(URL)
    r = r.json()
    accountId = r["accountId"]
    #print(accountId)
    return accountId

accountId = getAccountId('arantir', API_KEY)
# now we need matchId from the last 10 games
def getMatchId(accountId, API_KEY):
    CONST_MATCH_NUMBERS = 10
    CONST_RANKED_QUEUE_ID = 440
    # 440 = flex
    # 420 = ranked
    i = 0
    URL = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/'+accountId+'?api_key='+API_KEY
    r = requests.get(URL)
    r = r.json()
    a = [accountId]
    for x in range(len(r['matches'])):
        if (i == CONST_MATCH_NUMBERS): 
            break
        if (r['matches'][x]["queue"] == CONST_RANKED_QUEUE_ID):
            a.append(r['matches'][x]['gameId'])
            i += 1
    return a
    
# matchList = [accountId, match1, match2, ..., matchN]
matchList = getMatchId(accountId, API_KEY)
print(matchList)

def getGoldPerMin(matchList, API_KEY):
    a = [matchList[0]]
    b = []
    accountId = matchList[0]
    CONST_PLAYERS_PER_MATCH = 10
    c = csv.writer(open("csv/GOLDPERMIN.csv", "w"), lineterminator='\n')
    #print(len(matchList))
    for x in range(len(matchList) - 1):
        b.append(0)
        matchId = matchList[x + 1]
        URL = 'https://na1.api.riotgames.com/lol/match/v4/matches/'+str(matchId)+'?api_key='+API_KEY
        r = requests.get(URL)
        r = r.json()
        participantId = 0
        for y in range(CONST_PLAYERS_PER_MATCH):
            if (r['participantIdentities'][y]['player']['accountId'] == accountId):
                participantId = r['participantIdentities'][y]['participantId']
        #print(participantId)
        win = r['participants'][participantId - 1]['stats']['win']
        for y in range(CONST_PLAYERS_PER_MATCH):
            if (r['participants'][y]['stats']['win'] == win):
                myDict = r['participants'][y]['timeline']["goldPerMinDeltas"]
                last = list(myDict.keys())[-1]
                #print(r['participants'][y]['timeline']["goldPerMinDeltas"][last])
                b[x] = b[x] + r['participants'][y]['timeline']["goldPerMinDeltas"][last]
        b[x] = b[x] / 5
        c.writerow([b[x]])
        myDict = r['participants'][participantId - 1]['timeline']["goldPerMinDeltas"]
        last = list(myDict.keys())[-1]
        a.append(r['participants'][participantId - 1]['timeline']["goldPerMinDeltas"][last])
    c = csv.writer(open("csv/SUMMONERGOLDPERMIN.csv", "w"), lineterminator='\n')
    for x in range(len(matchList) - 1):
        c.writerow([a[x + 1]])


getGoldPerMin(matchList, API_KEY)