import csv
import json
import math

def winLossRatio(league, division):
    with open('csv/'+league+''+division+'.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    length = len(data)
    i = 1
    winsSum = 0
    lossesSum = 0
    while i < length: 
        # print(data[i])
        winsSum = winsSum + int(data[i][0])
        lossesSum = lossesSum + int(data[i][1]) 
        i += 1
    totalMatches = winsSum + lossesSum
    winRatio = winsSum / totalMatches * 100
    lossRatio = (100 - winRatio)
    dictionary = {
        'League': league,
        'Division': division,
        'Win ratio': winRatio,
        'Loss Ratio': lossRatio
    }
    with open('JSON/winLossRatio.json', 'ab+') as f: # to be refactored
        f.seek(0, 2)
        if f.tell() == 0:
            f.write(json.dumps([dictionary], indent = 4, sort_keys = True).encode())
        else :
            f.truncate()
            f.seek(-1,2)
            f.truncate()
            f.write(' ,\n'.encode())
            f.truncate()
            f.write(json.dumps(dictionary, indent = 4, sort_keys = True).encode())
            f.write(']'.encode())
    return winRatio

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def binomialDistribution(winRatio):
    n = 10    # total
    p = winRatio / 100     # Probability
    k = 0  # number of success
    px = 0
    c = csv.writer(open("final_csv/binomial.csv", "w"), lineterminator='\n')
    c.writerow(['wins', 'loss'])
    CONST_CURVE_FIT = 0.003
    CONST_CURVE_FIT_SMALL = 0.00001
    while k <= n:
        px = nCr(n,k) * pow(p, k) * pow(1 - p, n - k)
        #c.writerow(px)
        print(px)
        c.writerow([k, px, px + (px * 0.05)])
        k += 1

win = winLossRatio('DIAMOND', 'IV')
binomialDistribution(win)

