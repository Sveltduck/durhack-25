from datetime import datetime
import numpy as np 
import networkx as nx

def overnightGuest(answer1, answer2):
    #that's fine = 2, I'd rather they didn't = 1, no way = 0
    if answer1 == answer2:
        return 1
    elif abs(answer1 - answer2) == 1:
        return 0.5
    else:
        return 0

def textSimilarity(answer1, answer2):
    SetAnswer1 = set(answer1.lower().split())
    SetAnswer2 = set(answer2.lower().split())
    rating = len(SetAnswer1 & SetAnswer2) / len(SetAnswer1 | SetAnswer2)
    return rating

def personalityType(answer1, answer2):
    if answer1 == answer2:
        return 1
    else:
        return 0

def tidiness(tidy1, tidy2, care1, care2):
    tidy1 = tidy1 / 5
    tidy2 = tidy2 / 5
    care1 = care1 / 5
    care2 = care2 / 5

    mutualTidiness = 1-abs(tidy1 - tidy2)
    agreeable1 = 1 - abs(tidy1 - care2)
    agreeable2 = 1 - abs(tidy2 - care1)


    compatibility = (agreeable1 +agreeable2 + mutualTidiness)/3
    return (round(compatibility,2))


def minutes(time):
    time = datetime.strptime(time, '%H:%M')
    return time.hour * 60 + time.minute

def timeSimilarity(time1, time2):
    difference = abs(minutes(time1) - minutes(time2))
    difference = min(difference, 1440 - difference)
    difference = 1 - difference / 480
    if difference < 0:
        return 0
    else:
        return difference



def weekdayTimings(sleep1, wake1, sleep2, wake2):
    sleep = timeSimilarity(sleep1, sleep2)
    wake = timeSimilarity(wake1, wake2)
    return(round((sleep + wake)/ 2, 2))

def workTimings(earliest1, latest1, earliest2, latest2):
        start = timeSimilarity(earliest1, earliest2)
        end = timeSimilarity(latest1, latest2)
        return(round((start - end) / 2, 2))

def nightOutTimings(sleep1, sleep2):
    return(timeSimilarity(sleep1, sleep2))

def overallTimings(weekdayScore, workScore, nightOutScore):
    return(round((weekdayScore + workScore + nightOutScore)/2,2))

def timingCompatibility(sleep1, sleep2, wake1, wake2, earliestwork1, earliestwork2, latestwork1, latestwork2, nightOutsleep1, nightOutsleep2):
    weekdayScore = weekdayTimings(sleep1, wake1, sleep2, wake2)
    workScore = workTimings(earliestwork1, latestwork1, earliestwork2, latestwork2)
    nightOutScore = nightOutTimings(nightOutsleep1, nightOutsleep2)
    result = overallTimings(weekdayScore, workScore, nightOutScore)
    return (result)

def finalCompatibility(person1, person2):
    guest = overnightGuest(answer1, answer2)
    music = textSimilarity(musicAnswer1, musicAnswer2)
    sport = textSimilarity(sportAnswer1, sportAnswer2)
    personality = personalityType(type1, type2)
    cleanliness = tidiness(tidy1, tidy2, care1, care2)
    times = timingCompatibility(sleep1, sleep2, wake1, wake2, earliestwork1, earliestwork2, latestwork1, latestwork2, nightOutsleep1, nightOutsleep2)
    compatibility = (guest + music +sport +personality + cleanliness + times)
    return compatibility



def averageMatrix(tab):
    mat=[["" for y in range(len(tab))] for x in range(len(tab))  ]


    for i in range(len(tab)):

        for j in range(i,len(tab)):
            a= (tab[i][j] +tab[j][i])/2
            mat[i][j],mat[j][i]=a,a
    return np.array(mat) 

def getRoomates(matrix, entryOrder):

    numbersToNames=dict(zip([x for x in range(len(entryOrder))], entryOrder))


    G=nx.from_numpy_array(averageMatrix(matrix))
    a=nx.max_weight_matching(G, maxcardinality=False)
    named=[]
    for item in a :
        named.append((numbersToNames[item[0]], numbersToNames[item[1]])    )
       
    print(named)
    return named

def getBestMatches(n,matrix,entryOrder):
    numbersToNames=dict(zip([x for x in range(len(entryOrder))], entryOrder))
    compDict= dict(zip([x for x in range(len(matrix[n]))] ,matrix[n] )) 

    numsInOrder=sorted(compDict.items(),key=lambda item:item[1],reverse=True)
    numsInOrder=([numbersToNames[x[0]] for x in numsInOrder[:-1]])
    return numsInOrder[:5]
  












#need empty matrix size of n where n is number of people