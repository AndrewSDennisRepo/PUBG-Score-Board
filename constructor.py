

import json
import pprint
import numpy as np


import pandas as pd



def build_position_frame(telemetry, team):
    details = []
    for item in telemetry['telemetry']:
        frame = {}
        if item["_T"] == 'LogPlayerPosition' and team in item['character']['name']:
            frame['matchId'] = telemetry['match_id']
            # frame['tournament'] = frame['tournament']
            frame['name'] = item['character']['name']
            frame['health'] = item['character']['health']
            frame['timeStamp'] = item['_D']
            frame['elapsedTime'] = item['elapsedTime']
            frame['ranking'] = item['character']['ranking']
            frame['numAlivePlayers'] = item['numAlivePlayers']
            frame['positionVector'] = [item['character']['location']['x'], item['character']['location']['y'], item['character']['location']['z']]
            frame['xPos'] = item['character']['location']['x']
            frame['yPos'] = item['character']['location']['y']
            frame['zPos'] = item['character']['location']['z']
            details.append(frame)
    return details


def telem_match_build(fr):
    df = pd.DataFrame(fr)
    maxTime = max(df['elapsedTime'])
    groupTime = int(maxTime / 30)

    bins = []
    labels = []
    t = groupTime
    for i in range(1, 31):
        bins.append(t)
        labels.append(i)
        t = t + groupTime

    bins = bins + [maxTime]
    labels = labels


    df['binned'] = pd.cut(df['elapsedTime'], bins=bins, labels=labels)
    dfg = df.groupby(['name', 'binned', 'matchId'])[['xPos', 'yPos', 'zPos']].mean().reset_index()
    
    players = dfg['name'].unique()
    bins = dfg['binned'].unique()

    build = []
    for i in bins:
        dff = dfg[dfg['binned'] == i]
        dff['y_centroid'] = dff['yPos'].mean()
        dff['x_centroid'] = dff['xPos'].mean()
        dff['z_centroid'] = dff['zPos'].mean()
        player_build = []
        for n in players:
            dfn = dff[dff['name'] == n]
            player_point = np.asarray([dfn['yPos'], dfn['xPos'], dfn['zPos']])
            centroid = np.asarray([dfn['y_centroid'], dfn['x_centroid'], dfn['z_centroid']])
            dfn[str(i) + '_' + n + '_dist'] = np.linalg.norm(player_point - centroid)
            player_build.append(dfn)
        build.append(pd.concat(player_build))

    dfg = pd.concat(build)
    dfg2 = dfg.groupby('matchId').sum().reset_index()
    return dfg2


def telem_dataset(js, team):
    newer = []
    matcher = []
    for item in js:
        try:
            fr = build_position_frame(item, team)
            match = match_info_build(item)
            out = telem_match_build(fr)
            newer.append(out)
            matcher.append(match)
            print('Match Complete....')
        except:
            print('Failed a Match or something.....')
    telem = pd.concat(newer)
    match_i = pd.concat(matcher)

    df = telem.merge(match_i, on='matchId', how='left')
    return df


def match_info_build(js2):
    match_ = []
    for item in js2['match_info']['included']:
        try:
            if 'STK' in item['attributes']['stats']['name']:
                framer = {}
                framer['matchId'] = js2['match_id']
                framer['winPlace'] = item['attributes']['stats']['winPlace']
                framer['distance'] = item['attributes']['stats']['walkDistance'] + item['attributes']['stats']['rideDistance'] + item['attributes']['stats']['swimDistance']
                framer['damageDealt'] = item['attributes']['stats']['damageDealt']
                framer['kills'] = item['attributes']['stats']['kills']
                framer['heals'] = item['attributes']['stats']['heals']
                framer['boosts'] = item['attributes']['stats']['boosts']
                match_.append(framer)
        except:
            pass

    dfm = pd.DataFrame(match_)

    dfmg = dfm.groupby('matchId').agg({'winPlace': 'mean', 'distance': 'sum', 'distance': 'sum', 'damageDealt':'sum', 'kills':'sum', 'heals':'sum', 'boosts':'sum'}).reset_index()
    return dfmg


with open(r'E:\PUBG_API\tourn_data.json') as fh:
    js = json.load(fh)


df = telem_dataset(js, 'STK')

# print(df)
df.to_csv(r'E:\PUBG_API\dist_file2.csv', index=False)

# path = r'E:\PUBG_API\matches\cc7218b3-42ff-4203-a88d-fabebf245cac.json'

# with open(path) as f:
#     js2 = json.load(f)
# print(dfmg)