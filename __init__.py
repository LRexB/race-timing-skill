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
        race_id =  '2023-10-27T15:37:30.519419 - finish, lap 1'
        race_result_doc = races_ref.document(race_id)
        race_result_data = race_result_doc.get().to_dict()
        self.log.info("got races")
        self.log.info(race_result_data)
        for bib_number in race_result_data.keys() : #{'1', '2', '7'} :
            bib = race_result_data[bib_number]['bibNumber']
            time = race_result_data[bib_number]['chipTime']
            self.log.info(f"{bib_number} => {bib} => {time}")
            self.speak_dialog('timing.race', data= {'bib1':bib, 'time1' : time})


def create_skill():
    return RaceTiming()

