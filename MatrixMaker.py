from datetime import datetime
import numpy as np 
import networkx as nx
import psycopg2

conn = psycopg2.connect(
   "postgres://99daed4eb57ee8d15df095e80006a1a2b9d921d26366b67f4ad069055d386ae5:sk_eYTLTQN0oFInIQVT0gM7C@db.prisma.io:5432/postgres?sslmode=require"
   
   )

cur=conn.cursor()



cur.execute('SELECT * FROM "Answers";')

rows=cur.fetchall()



cur.execute(('SELECT "studentId" FROM "Answers";'))
ids=cur.fetchall()

ids=[x[0] for x in ids]





def overnightGuest(answer1, answer2):
    #that's fine = 2, I'd rather they didn't = 1, no way = 0
    answer2=answer2
    answer1=answer1

    answer1,answer2= {"yes":1,'rather-no':0.5,'no':0}[answer1], {"yes":1,'rather-no':0.5,'no':0}[answer2]

    print(answer1)
    if answer1 == answer2:
        return 1
    elif abs(answer1 - answer2) == 1:
        return 0.5
    else:
        return 0

def textSimilarity(answer1, answer2):

    
    print(answer1)
    SetAnswer1 = set([x.lower() for x in answer1])
    SetAnswer2 = set([x.lower() for x in answer2])
    rating = max(len(SetAnswer1 & SetAnswer2),1) /max( len(SetAnswer1 | SetAnswer2),1)
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
    
    
    #time=str(time[0][0])

    
   
    return time  *30
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
from psycopg2.extras import RealDictCursor

def finalCompatibility(person1, person2):
    curr=conn.cursor(cursor_factory=RealDictCursor)
    curr.execute('SELECT * FROM "Answers" WHERE "studentId" = %s;', (person1,))
    all1 = curr.fetchone()
    print(all1.keys())

    curr.execute('SELECT * FROM "Answers" WHERE "studentId" = %s;', (person2,))
    all2 = curr.fetchone()

    guest = overnightGuest(all1["overnightGuests"], all2["overnightGuests"])
    musicG = textSimilarity(all1["musicArtists"], all2["musicArtists"])
    musicA = textSimilarity(all1["musicGenres"], all2["musicGenres"])
    sport  = textSimilarity(all1["sportsWatched"], all2["sportsWatched"])
    personality = personalityType(all1["introvertExtrovert"], all2["introvertExtrovert"])
    cleanliness=  tidiness(all1["tidiness"],all2["tidiness"],all1["careAboutTidiness"],all2["careAboutTidiness"])
    
    sleep1          =all1["normalWeekdayBedtime" ]
    wake1           =all1[ "normalWeekdayStartTime"]
    earliestwork1  =all1["workStartTime"]
    latestwork1     =all1["workEndTime"]
    nightOutsleep1  =all1["nightOutBedtime"]
  
  
    sleep2          =all2["normalWeekdayBedtime" ]
    wake2           =all2[ "normalWeekdayStartTime"]
    earliestwork2  =all2["workStartTime"]
    latestwork2     =all2["workEndTime"]
    nightOutsleep2  =all2["nightOutBedtime"]
    



    times = timingCompatibility(sleep1, sleep2, wake1, wake2, earliestwork1, earliestwork2, latestwork1, latestwork2, nightOutsleep1, nightOutsleep2)















    compatibility = (guest + musicG+musicA +sport +personality + cleanliness + times)
    return compatibility



def averageMatrix(tab):
    mat=[["" for y in range(len(tab))] for x in range(len(tab))  ]


    for i in range(len(tab)):

        for j in range(i,len(tab)):
            a= (tab[i][j] +tab[j][i])/2
            mat[i][j],mat[j][i]=a,a
    return np.array(mat) 

def getRoomates(matrix, entryOrder=None):

    if entryOrder==None:
        cur.execute('SELECT "name" from "User"')
        entryOrder=cur.fetchall()
        entryOrder=[x[0] for x in entryOrder]
        
    numbersToNames=dict(zip([x for x in range(len(entryOrder))], entryOrder))


    G=nx.from_numpy_array(averageMatrix(matrix))
    a=nx.max_weight_matching(G, maxcardinality=False)
    named=[]
    for item in a :
        named.append((str( ids[item[0]] ), str( ids [item[1]])  )    )
       
    namedDict={}
    print(named)
    for item in named:
        namedDict[item[0]]=item[1]
        namedDict[item[1]]=item[0]
    return namedDict

def getBestMatches(n,matrix,entryOrder):
    numbersToNames=dict(zip([x for x in range(len(entryOrder))], entryOrder))
    compDict= dict(zip([x for x in range(len(matrix[n]))] ,matrix[n] )) 

    numsInOrder=sorted(compDict.items(),key=lambda item:item[1],reverse=True)
    numsInOrder=([numbersToNames[x[0]] for x in numsInOrder[:-1]])
    return numsInOrder[:5]





def populateMatrix():
    #get size of matrix = n
    matrix = [[0 for i in range(len(ids))] for j in range(len(ids))]

    for i in range(len(ids)) :
        for j  in range(i,len(ids)):
            #get gender
            person1=ids[i]
            person2=ids[j]

            cur.execute('SELECT "gender" FROM "Answers" Where "studentId" =%s;',(person1,))
            genderi=cur.fetchall()

            cur.execute('SELECT "gender" FROM "Answers" Where "studentId" =%s;',(person2,))
            genderj=cur.fetchall()


            if i == j:
                matrix[i][j] = 0
            elif genderi!= genderj:
                matrix[i][j] = 0
            else:
                comp = finalCompatibility(person1, person2)
                matrix[i][j] = comp
                matrix[j][i] = comp

    return matrix


from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading


def compute_roommates():
    m = populateMatrix()
    if len(m) > 0:
        return getRoomates(m)
    else:
        return {}



class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/roommates":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            # Convert your Python dict to JSON
            response = json.dumps(compute_roommates())
            self.wfile.write(response.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

def run_server():
    server = HTTPServer(("0.0.0.0", 8080), MyRequestHandler)
    print("Server started at http://localhost:8080")
    server.serve_forever()

# Start server in background thread (so your code can still run other things)
threading.Thread(target=run_server, daemon=True).start()







#need empty matrix size of n where n is number of people