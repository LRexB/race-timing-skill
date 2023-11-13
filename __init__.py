from mycroft import MycroftSkill, intent_file_handler


class RaceTiming(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('timing.race.intent')
    def handle_timing_race(self, message):
        self.speak_dialog('timing.race')


def create_skill():
    return RaceTiming()

