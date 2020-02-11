import csv

with open('csv/DIAMONDIII.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
length = len(data)
i = 1
winsSum = 0
lossesSum = 0
while i < length: 
    print(data[i])
    winsSum = winsSum + int(data[i][0])
    lossesSum = lossesSum + int(data[i][1]) 
    i += 1
totalMatches = winsSum + lossesSum
winRatio = winsSum / totalMatches
lossRatio = 1 - winRatio
print(winRatio * 100)
print(lossRatio * 100)