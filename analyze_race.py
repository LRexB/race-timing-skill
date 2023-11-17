
import firebase_admin
from firebase_admin import firestore

debug = False

def get_best_times() :
    best_time_list = {}
    app = firebase_admin.initialize_app()
    db = firestore.client()
    racesRef = db.collection('races')
    for race_id in racesRef.stream():
        if debug : print(f"got race: {race_id.id}")
        if not best_time_list :
            best_time_list = race_id.to_dict()
        else :
            new_times = race_id.to_dict()
            for lapNumber in sorted(new_times.keys()):
                lapResults = new_times[lapNumber]
                best_lap_times = best_time_list[lapNumber]
                for bibNumber in lapResults.keys() :
                    if bibNumber in best_lap_times.keys() :
                        rssi1 = best_lap_times[bibNumber]['rssiValue']
                        rssi2 = lapResults[bibNumber]['rssiValue']
                        if debug : print (f" for bib {bibNumber}, rssi1: {rssi1}, rssi2: {rssi2}")
                        if rssi2 > rssi1 :
                            best_lap_times[bibNumber]['rssiValue'] = rssi2
                            best_lap_times[bibNumber]['currentTick'] = lapResults[bibNumber]['currentTick']
                            best_lap_times[bibNumber]['chipTime'] = lapResults[bibNumber]['chipTime']
                            if debug : print (f"reseting bib {bibNumber} time")
                    else :
                        best_lap_times[bibNumber] = lapResults[bibNumber]


    return best_time_list

timeList = {}
lapResults = {}


raceResultData = get_best_times()
for lapNumber in sorted(raceResultData.keys()) :
    lapResults = raceResultData[lapNumber]
    if lapNumber == '0' :
        if debug : print("setting start")
        for bibNumber in lapResults.keys() : 
            bibList = {}
            bibList['startTick'] = bibList['lastLapTime'] = lapResults[bibNumber]['currentTick']
            bib = lapResults[bibNumber]['bibNumber']
            bibList['startTime'] = lapResults[bibNumber]['startTime']
            timeList[bibNumber] = bibList
            if debug : print(f"{lapNumber} = >{bibNumber} => {bib} => {timeList[bibNumber]}")
    else :
        if debug : print(f"setting lap {lapNumber}")
        for bibNumber in lapResults.keys() :
            bib = lapResults[bibNumber]['bibNumber']
            time = (lapResults[bibNumber]['currentTick'] - timeList[bibNumber]['lastLapTime'])/1000
            timeList[bibNumber]['lastLapTime'] = lapResults[bibNumber]['currentTick']
            print(f"{lapNumber} = >{bibNumber} => {bib} => {time} seconds")

print("end race")
lapNumber = 'final'
for bibNumber in lapResults.keys() : 
    bib = lapResults[bibNumber]['bibNumber']
    time = (timeList[bibNumber]['lastLapTime'] - timeList[bibNumber]['startTick'])/1000
    print(f"{lapNumber} = >{bibNumber} => {bib} => {time} seconds")

