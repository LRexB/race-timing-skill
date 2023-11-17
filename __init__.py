from mycroft import MycroftSkill, intent_file_handler
import firebase_admin
from firebase_admin import firestore

class RaceTiming(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        app = firebase_admin.initialize_app()
        self.db = firestore.client()

    @intent_file_handler('timing.race.intent')
    def handle_timing_race(self, message):
        racesRef = self.db.collection('races')
        race_id =  'race start'
        raceResultDoc = racesRef.document(race_id)
        raceResultData = raceResultDoc.get().to_dict()
        self.log.info("got races")
        self.log.info(raceResultData)
        timeList = {}
        lapResults = {}

        for lapNumber in sorted(raceResultData.keys()) :
            lapResults = raceResultData[lapNumber]
            if lapNumber == '0' :
                self.log.info("setting start")
                for bibNumber in lapResults.keys() : 
                    bibList = {}
                    bibList['startTick'] = bibList['lastLapTime'] = lapResults[bibNumber]['currentTick']
                    bib = lapResults[bibNumber]['bibNumber']
                    bibList['startTime'] = lapResults[bibNumber]['startTime']
                    timeList[bibNumber] = bibList
                    self.log.info(f"{lapNumber} = >{bibNumber} => {bib} => {timeList[bibNumber]}")
            else :
                self.log.info(f"setting lap {lapNumber}")
                for bibNumber in lapResults.keys() :
                    bib = lapResults[bibNumber]['bibNumber']
                    time = (lapResults[bibNumber]['currentTick'] - timeList[bibNumber]['lastLapTime'])/1000
                    timeList[bibNumber]['lastLapTime'] = lapResults[bibNumber]['currentTick']
                    self.log.info(f"{lapNumber} = >{bibNumber} => {bib} => {time}")
                    self.speak_dialog('timing.race', data= {'lap1': lapNumber, 'bib1':bib, 'time1' : time})

        self.log.info("end race")
        for bibNumber in lapResults.keys() : 
            bib = lapResults[bibNumber]['bibNumber']
            time = (timeList[bibNumber]['lastLapTime'] - timeList[bibNumber]['startTick'])/1000
            self.log.info(f"{lapNumber} = >{bibNumber} => {bib} => {time}")
            self.speak_dialog('timing.race', data= {'lap1': 'final', 'bib1':bib, 'time1' : time})

def create_skill():
    return RaceTiming()

