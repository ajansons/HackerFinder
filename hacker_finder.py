import json

suspicious_long_range_weapons = {
  "WeapBerreta686_C": "S686",
  "WeapG18_C": "P18C",
  "WeapM1911_C": "P1911",
  "WeapM9_C": "P92",
  "WeapSaiga12_C": "S12K",
  "WeapSawnoff_C": "Sawed-off",
  "WeapThompson_C": "Tommy Gun",
  "WeapUMP_C": "UMP9",
  "WeapUZI_C": "Micro Uzi",
  "WeapVector_C": "Vector",
  "Weapvz61Skorpion_C": "Skorpion",
  "WeapWinchester_C": "S1897"
 }

class HackerFinder:

    def __init__(self, telem, distance_threshold=15000):
        self.telem = telem
        self.distance_threshold = distance_threshold

    def find_suspcious_assaults(self, weapons=suspicious_long_range_weapons, attack_duration=5):
        suspicious_events = [x for x in self.telem.knocks + self.telem.kills
                            if x['damageCauserName'] in suspicious_long_range_weapons and x['distance'] > self.distance_threshold]

        assaults = []
        for k in suspicious_events:
            attacker_type = 'attacker' if k['_T'] == 'LogPlayerMakeGroggy' else 'killer'
            damages = self.telem.get_prior_events(k, self.telem.get_damages_by_player(k[attacker_type]['name'], k['victim']['name']), attack_duration)
            attacks = self.telem.get_prior_events(k, self.telem.get_attacks_by_player(k[attacker_type]['name']), attack_duration)
            if damages:
                assaults.append(
                {'event': k,
                'damages': damages,
                'attacks': attacks
                })
        return assaults

    def find_suspcious_assaults_by_player(self, name, weapons=suspicious_long_range_weapons, attack_duration=5):
        suspicious_events = [x for x in self.telem.get_knocks_by_player(name) + self.telem.get_kills_by_player(name)
                            if x['damageCauserName'] in suspicious_long_range_weapons and x['distance'] > self.distance_threshold]

        return [{'event': k,
        'damages': self.telem.get_prior_events(k, self.telem.get_damages_by_player(name, k['victim']['name']), attack_duration),
        'attacks': self.telem.get_prior_events(k, self.telem.get_attacks_by_player(name), attack_duration)
        } for k in suspicious_events]

    def summarise_assault(self, assault):
        assault_type, attacker_type = ('knocked out', 'attacker') if assault['event']['_T'] == 'LogPlayerMakeGroggy' else ('killed', 'killer')
        attacker = assault['event'][attacker_type]['name']
        victim = assault['event']['victim']['name']
        distance = int(assault['event']['distance'] / 100)
        gun = suspicious_long_range_weapons[assault['event']['damageCauserName']]
        hits = len(assault['damages'])
        headshot_percentage = "{0:.0%}".format(len([x for x in assault['damages'] if x['damageReason'] == 'HeadShot']) / len(assault['damages']))

        return("%s %s %s with a %s at %d metres. Out of the %d hits that landed, %s were headshots." 
        % (attacker, assault_type, victim, gun, distance, hits, headshot_percentage))

