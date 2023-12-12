from mycroft import MycroftSkill, intent_file_handler
import firebase_admin
from firebase_admin import firestore

class RaceTiming(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        app = firebase_admin.initialize_app()
        self.db = firestore.client()

    def get_best_times(self) :
        best_time_list = {}
        racesRef = self.db.collection('races')
        for race_id in racesRef.stream():
            self.log.debug(f"got race: {race_id.id}")
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
                            self.log.debug (f" for bib {bibNumber}, rssi1: {rssi1}, rssi2: {rssi2}")
                            if rssi2 > rssi1 :
                                best_lap_times[bibNumber]['rssiValue'] = rssi2
                                best_lap_times[bibNumber]['currentTick'] = lapResults[bibNumber]['currentTick']
                                best_lap_times[bibNumber]['chipTime'] = lapResults[bibNumber]['chipTime']
                                self.log.debug (f"reseting bib {bibNumber} time")
                        else :
                            best_lap_times[bibNumber] = lapResults[bibNumber]
        return best_time_list


    @intent_file_handler('timing.race.intent')
    def handle_timing_race(self, message):

        timeList = {}
        lapResults = {}
        raceResultData = self.get_best_times()
        self.log.info("got the race results")
        for lapNumber in sorted(raceResultData.keys()) :
            lapResults = raceResultData[lapNumber]
            if lapNumber == '0' :
                self.log.debug("setting start")
                for bibNumber in lapResults.keys() : 
                    bibList = {}
                    bibList['startTick'] = bibList['lastLapTime'] = lapResults[bibNumber]['currentTick']
                    bib = lapResults[bibNumber]['bibNumber']
                    bibList['startTime'] = lapResults[bibNumber]['startTime']
                    timeList[bibNumber] = bibList
                    self.log.debug(f"{lapNumber} = >{bibNumber} => {bib} => {timeList[bibNumber]}")
            else :
                self.log.debug(f"setting lap {lapNumber}")
                for bibNumber in lapResults.keys() :
                    bib = lapResults[bibNumber]['bibNumber']
                    time = (lapResults[bibNumber]['currentTick'] - timeList[bibNumber]['lastLapTime'])/1000
                    timeList[bibNumber]['lastLapTime'] = lapResults[bibNumber]['currentTick']
                    self.speak_dialog('timing.race', data= {'lap1': lapNumber, 'bib1':bib, 'time1' : time})
        self.log.info("end race")
        lapNumber = 'final'
        for bibNumber in lapResults.keys() : 
            bib = lapResults[bibNumber]['bibNumber']
            time = (timeList[bibNumber]['lastLapTime'] - timeList[bibNumber]['startTick'])/1000
            self.speak_dialog('timing.race', data= {'lap1': 'final', 'bib1':bib, 'time1' : time})

def create_skill():
    return RaceTiming()

