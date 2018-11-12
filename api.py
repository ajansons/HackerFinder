import requests
import json

class Api:

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.json_headers = {"Accept": "application/json"}
        self.auth_headers = {**self.json_headers, **{"Authorization":"Bearer %s" % self.api_key}}

    def get_telem_data_by_match_id(self, match_id):
        match_url = "https://api.pubg.com/shards/steam/matches/%s" % match_id
        match_res = requests.get(match_url, headers={'Accept': 'application/json'})
        match_data = json.loads(match_res.content)
        telem_url = [x for x in match_data['included'] if 'URL' in x['attributes']][0]['attributes']['URL']
        telem_res = requests.get(telem_url, headers=self.json_headers)
        return json.loads(telem_res.content)

    def get_sample_match_ids(self, region="pc-sea"):
        url = "https://api.pubg.com/shards/%s/samples" % region
        headers = self.auth_headers
        res = requests.get(url, headers=headers)
        data = json.loads(res.content)
        return [x['id'] for x in data['data']['relationships']['matches']['data'] if x['type'] == 'match']

    def get_match_ids_by_player(self, name, platform='steam'):
        url = "https://api.pubg.com/shards/%s/players?filter[playerNames]=%s" % (platform, name)
        res = requests.get(url, headers=self.auth_headers)
        data = json.loads(res.content)
        return [x['id'] for x in data['data'][0]['relationships']['matches']['data'] if x['type'] == 'match']