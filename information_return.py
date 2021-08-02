
import os
import requests
import json
import re
import time
from pubg_python import PUBG, Shard
from key import key

api_key = os.getenv('PUBG')


url = 'https://api.pubg.com/tournaments'

pubg_api = PUBG(key, Shard.PC_TOURNAMENT)

header = {"Authorization": "Bearer {}".format(key),
          "Accept": "application/vnd.api+json"
}

class API:
    def __init__(self, key, header, base_url):
        self.key = key
        self.header = header
        self.url = base_url
        self._tournaments = None
        self._matches = None
        self._data = None

    def tournaments(self, tournaments):
        _tournaments = []
        for tourn in tournaments:   
            req = requests.get(self.url +'/' + tourn, headers=self.header)
            tournaments_ = json.loads(req.text)
            _tournaments.append(tourn)
        return _tournaments

    def matches(self, tournament):
        # if self._matches is None:
        _matches = []
        for tourn in tournament:
            try:
                match_set = {}
                mreq = requests.get(self.url + '/' + tourn, headers=self.header)
                matches_ = json.loads(mreq.text)

                match_set['matches'] = matches_['data']['relationships']['matches']['data']
                match_set['tournament'] = tourn
                _matches.append(match_set)
            except:
                print('Pass')
        return _matches
    
    def data(self, tournament):
        # if self._data is None:
        _data = []
        for tournament in self.matches(tournament):
            print('Processing Tournament: ', tournament['tournament'])
            for match in tournament['matches']:
                new_frame = {}
                new_frame['tournament'] = tournament['tournament']
                new_frame['match_id'] = match['id']
                print('Processing Match: ', match['id'])
                new_url = 'https://api.pubg.com/shards/tournament/matches/' + match['id']
                nreq = requests.get(new_url, headers=self.header)
                info = json.loads(nreq.text)
                new_frame['match_info'] = info
                telem = pubg_api.matches().get(match['id'])
                treq = requests.get(telem.assets[0].url)
                new_frame['telemetry'] = json.loads(treq.text)
                with open(r"D:\PUBG-Score-Board\2021\winnerA\\" + match['id'] + '.json', 'w') as f:
                    f.write(json.dumps(new_frame))
                _data.append(new_frame)
        return _data


tournaments = ['am-pcs4w1', 'am-pcs4w2', 'am-pcs4w3', 'am-eslm2', 'eu-pcs4w1', 'eu-pcs4w2', 'eu-pcs4w3', 'eu-eslm2']



client = API(key, header, url)

# for t in tournaments:
client.data(tournaments)
