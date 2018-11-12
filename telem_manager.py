import json
import datetime

class TelemManager:

    def __init__(self, telem_data=None, file=None):
        self.telem = json.load(file) if file != None else telem_data
        self.equips = self.get_events_by_type('LogItemEquip')
        self.kills = self.get_events_by_type('LogPlayerKill')
        self.attacks = self.get_events_by_type('LogPlayerAttack')
        self.damages = self.get_events_by_type('LogPlayerTakeDamage')
        self.knocks = self.get_events_by_type('LogPlayerMakeGroggy')

    def get_attacks_by_player(self, name):
        return [x for x in self.attacks if x['attacker']['name'] == name]

    def get_damages_by_player(self, name, victim=None):
        return [x for x in self.damages
               if x['attacker'] != None and x['attacker']['name'] == name and (x['victim']['name'] == victim or victim == None)]

    def get_knocks_by_player(self, name):
        return [x for x in self.knocks if x['attacker']['name'] == name]

    def get_kills_by_player(self, name):
        return [x for x in self.kills if x['killer']['name'] == name]

    def get_events_by_type(self, event_type):
        return [x for x in self.telem if x['_T'] == event_type]

    def get_prior_events(self, event, events, seconds_before):
        def x_happened_n_seconds_before_y(x, y, n):
            difference = x - y
            seconds = difference.seconds
            return(seconds >= 0 and seconds <= n)

        event_timestamp = self.timestamp_to_datetime(event['_D'])
        return [x for x in events 
               if x_happened_n_seconds_before_y(event_timestamp, self.timestamp_to_datetime(x['_D']), seconds_before)]

    def timestamp_to_datetime(self, timestamp):
        return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')

    def get_match_id(self):
        match_string = self.telem[0]['MatchId']
        return match_string.split('.')[-1]