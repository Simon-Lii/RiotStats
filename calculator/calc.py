import csv
import json
import math
import statistics

def winLossRatio(league, division):
    with open('csv/'+league+''+division+'.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    length = len(data)
    i = 1
    win = 0
    loss = 0
    totalWinRatio = 0
    while i < length: 
        # print(data[i])
        win = int(data[i][0])
        loss= int(data[i][1]) 
        totalWinRatio = totalWinRatio + (win / (win + loss))
        i += 1
    #print(i)
    winRatio = totalWinRatio / i * 100
    #print(winRatio)
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

def testNormalityWinRatio(sample):
    i = 1
    count = 0
    scale = 0
    c = csv.writer(open("data.csv", "w"), lineterminator='\n')
    c.writerow(['district','nonlearner','learner'])
    while i < len(sample): 
        if (sample[i - 1] >= scale and sample[i - 1] <= scale + 2.5):
            count+=1
            i+=1 
        else:
            c.writerow([scale - 1, count])
            count = 0
            scale+=2.5

def winRatioPerSummoner(league, division, winRatio):
    with open('csv/'+league+''+division+'.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    length = len(data)
    i = 1
    ratio = 0
    totalRatio = 0
    win = 0
    loss = 0
    sample = []
    c = csv.writer(open("data.csv", "w"), lineterminator='\n')
    c.writerow(['district','nonlearner','learner'])
    while i < length: 
        # print(data[i])
        win = int(data[i][0])
        loss = int(data[i][1])
        ratio = win / (win + loss) * 100
        totalRatio = totalRatio + ratio
        sample.append(ratio)
        #print(ratio)
        #c.writerow([i, ratio, ratio + (ratio * 0.05)])
        i += 1
    a = sample
    mean = statistics.mean(sample)
    std_dev = math.sqrt(statistics.variance(sample, mean))
    minimum = 0
    #print(mean)
    maximum = 100
    CONST_REDUCE_LAG = 1
    if (length > 10000):
        CONST_REDUCE_LAG = 5
    scale = (maximum - minimum) / length * CONST_REDUCE_LAG
    index = minimum
    sample.sort()
    #print(mean)
    #print(sample[1664])
    i = 1
    px = 0
    while i < length / CONST_REDUCE_LAG:
        px = (1 / (std_dev * math.sqrt(2 * math.pi))) * math.exp((- 1 / 2) * math.pow((index - mean) / std_dev, 2))
        if (index < mean):
            c.writerow([round(index,2),0,px])
        else:
            c.writerow([round(index,2),px,0])
        i += 1
        index = index + scale
    return a
    #print(mean)
    #print(statistics.median(sample))
    #print(i)
    #print(std_dev)
    #print(mean)

def binomialDistribution(winRatio):
    n = 10    # total
    p = winRatio / 100     # Probability
    k = 0  # number of success
    px = 0
    c = csv.writer(open("final_csv/binomial.csv", "w"), lineterminator='\n')
    c.writerow(['wins', 'loss'])
    CONST_CURVE_FIT = 0.05
    while k <= n:
        px = nCr(n,k) * pow(p, k) * pow(1 - p, n - k)
        c.writerow([k, px, px + (px * CONST_CURVE_FIT)])
        k += 1

league = 'DIAMOND'
division = 'III'
win = winLossRatio(league, division)
#binomialDistribution(win)
sample = winRatioPerSummoner(league, division, win)

def normalGoldPerMin():
    sample = []
    with open('csv/SUMMONERGOLDPERMIN.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        sample = sum(data, [])
        sample = list(map(float, sample))
    length = len(sample)
    #print(sample)
    c = csv.writer(open("data.csv", "w"), lineterminator='\n')
    c.writerow(['district','nonlearner','learner'])
    my_mean = statistics.mean(sample)
    #print(my_mean)
    with open('csv/GOLDPERMIN.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        sample = sum(data, [])
        sample = list(map(float, sample))
    mean = statistics.mean(sample)
    std_dev = math.sqrt(statistics.variance(sample, mean))
    i = 0
    minimum = 0
    maximum = 700
    CONST_SEMI_SCALE = 350
    scale = ((maximum - minimum) / length) / CONST_SEMI_SCALE
    index = minimum
    sample.sort()
    i = 0
    px = 0
    while i < length * CONST_SEMI_SCALE:
        px = (1 / (std_dev * math.sqrt(2 * math.pi))) * math.exp((- 1 / 2) * math.pow((index - mean) / std_dev, 2))
        if (index < my_mean):
            c.writerow([round(index,2),0,px])
        else:
            c.writerow([round(index,2),px,0])
        index = index + scale
        i+=1

# normalGoldPerMin()
# test for normality:
# testNormalityWinRatio(sample)