import pandas as pd 
import subprocess
import json

from pubg_python import PUBG, Shard
from chicken_dinner.pubgapi import PUBGCore, PUBG

key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
eyJqdGkiOiI5MGEwNzZlMC0xOWJkLTAxMzctYThiMy0wM\
mY1ZGQ2M2ExMTUiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF\
0IjoxNTUwOTQyNTY4LCJwdWIiOiJibHVlaG9sZSIsInRpdGx\
lIjoicHViZyIsImFwcCI6ImZpbmFsY2lyY2xlIn0.cq48UFC6\
qrH4dXW6uJSVZtRe_sx7yDmrUKNYCsJnq0c'

pubg = PUBG(key, "xbox-na")


def search_player_match(player_name, max_matches):
    match_list = []
    num = 0
    while num <= max_matches:
        account_id = pubg.players_from_names(player_name)[0]
        recent_match = account_id.match_ids[num]
        num += 1
        match_list.append(recent_match)
    return match_list   


def match_detail_payload(match_list):
    payload = []
    for match in match_list:
        command = 'curl -X GET "https://api.pubg.com/shards/xbox/matches/\
        '+match+'" -H "accept: application/vnd.api+json"'
        p = subprocess.Popen(command,
                        shell=True,
                        stdout=subprocess.PIPE, 
                        stderr= subprocess.PIPE)
        out, err = p.communicate()
        payload.append(json.loads(out))
    return payload


def create_score_board(player_name):
    dataframe_set = []
    payload = match_detail_payload(
        search_player_match(player_name, 2))
    for model in payload:
        data = model["included"]
        maps = model['data']['attributes']['mapName']
        create_time = model['data']['attributes']['createdAt']
        player = []
        att = []
        for x in data:
            att.append(x['attributes'])
        for n in att:
            try:
                keys = ['name','kills','winPlace']
                dic = {x:n['stats'][x] for x in keys}
                dic['Map'] = maps
                dic['Time']= create_time
                player.append(dic)
            except:
                pass
        clean = []
        for name in player:
            if name != None:
                clean.append(name)
        df = pd.DataFrame(clean)
        df_ray = df[['name', 'winPlace', 'kills', 'Map', 'Time']]
        dataframe_set.append(df_ray)
        scoreboard = pd.concat(dataframe_set)
    return scoreboard


print(create_score_board("BLiTz5"))

scores = create_score_board("BLiTz5")

scores.to_csv("E:\\PUBG_API\\scores.csv")
