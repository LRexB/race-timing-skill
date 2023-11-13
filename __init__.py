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
        races = races_ref.stream()
        self.log.info("got races")
        for race in races :
            self.log.info(f"{race.id} => {race.to_dict()}")
            bib = race.to_dict()['1']['bibNumber']
            time = race.to_dict()['1']['chipTime']
            self.speak_dialog('timing.race', data= {'bib1':bib, 'time1' : time})


def create_skill():
    return RaceTiming()

