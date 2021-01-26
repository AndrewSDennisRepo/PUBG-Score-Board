
import os
import requests
import json
import re
import time
from pubg_python import PUBG, Shard
from key import key

api_key = os.getenv('PUBG')


url = 'https://api.pubg.com/tournaments'

pubg_api = PUBG(api_key, Shard.PC_TOURNAMENT)

header = {"Authorization": "Bearer {}".format(api_key),
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

    @property
    def tournaments(self):
        if self._tournaments is None:
            self._tournaments = []
            req = requests.get(self.url, headers=self.header)
            tournaments_ = json.loads(req.text)
            for item in tournaments_['data']:
                if 'na-dhsw' in item['id'] or re.match('na-pcs\\d+gf', item['id']):
                    self._tournaments.append(item['id'])
        return self._tournaments

    @property
    def matches(self):
        if self._matches is None:
            self._matches = []
            for tourn in self.tournaments:
                match_set = {}
                mreq = requests.get(self.url + '/' + tourn, headers=self.header)
                matches_ = json.loads(mreq.text)
                match_set['matches'] = matches_['data']['relationships']['matches']['data']
                match_set['tournament'] = tourn
                self._matches.append(match_set)
        return self._matches
    
    @property
    def data(self):
        if self._data is None:
            self._data = []
            for tournament in self.matches:
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
                    with open(r"E:\PUBG_API\matches\\" + match['id'] + '.json', 'w') as f:
                        f.write(json.dumps(new_frame))
                    self._data.append(new_frame)
        return self._data
