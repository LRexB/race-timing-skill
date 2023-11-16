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
        races_ref = self.db.collection('races')
        race_id =  'race start'
        race_result_doc = races_ref.document(race_id)
        race_result_data = race_result_doc.get().to_dict()
        self.log.info("got races")
        self.log.info(race_result_data)
        time_list = {}
        lap_results = {}

        for lap_number in race_result_data.keys() :
            lap_results = race_result_data[lap_number]
            if lap_number == '0' :
                self.log.info("setting start")
                for bib_number in lap_results.keys() : 
                    bib_list = {}
                    bib_list['start_tick'] = bib_list['last_lap_time'] = lap_results[bib_number]['currentTick']
                    bib = lap_results[bib_number]['bibNumber']
                    bib_list['start_time'] = lap_results[bib_number]['startTime']
                    time_list[bib_number] = bib_list
                    self.log.info(f"{lap_number} = >{bib_number} => {bib} => {time_list[bib_number]}")
            else :
                self.log.info(f"setting lap {lap_number}")
                for bib_number in lap_results.keys() :
                    bib = lap_results[bib_number]['bibNumber']
                    time = (lap_results[bib_number]['currentTick'] - time_list[bib_number]['last_lap_time'])/1000
                    time_list[bib_number]['last_lap_time'] = lap_results[bib_number]['currentTick']
                    self.log.info(f"{lap_number} = >{bib_number} => {bib} => {time}")
                    self.speak_dialog('timing.race', data= {'lap1': lap_number, 'bib1':bib, 'time1' : time})

        self.log.info("end race")
        for bib_number in lap_results.keys() : 
            bib = lap_results[bib_number]['bibNumber']
            time = (time_list[bib_number]['last_lap_time'] - time_list[bib_number]['start_tick'])/1000
            self.log.info(f"{lap_number} = >{bib_number} => {bib} => {time}")
            self.speak_dialog('timing.race', data= {'lap1': 'final', 'bib1':bib, 'time1' : time})


def create_skill():
    return RaceTiming()

