
import os
import json

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib import patheffects
from matplotlib import rc
import pandas as pd

from circle_position import split_

from constants import *

def map_name(file):
	return file['match_info']['data']['attributes']['mapName']



def player_coordinates(file, team, match_id):
	coord = []
	for item in file['telemetry']:
		field = {}
		if item['_T'] == 'LogPlayerPosition' and team in item['character']['name']:
			field['match_id'] = match_id
			field['player'] = item['character']['name']
			field['timeElapsed'] = item['elapsedTime']
			field['x'] = item['character']['location']['x']
			field['y'] = item['character']['location']['y']
			coord.append(field)
	return coord


def heavy_splitter(path, team):

	erang = []
	mira = []
	match_path = path + 'finals\\'

	files = os.listdir(match_path)
	print(len(files))
	for dex, file in enumerate(files):
		js = open(match_path + file)
		js = json.load(js)
		settings = player_coordinates(js, team, dex)
		if map_name(js) == 'Baltic_Main':
			erang.append(settings)
		else:
			mira.append(settings)
	return mira, erang





path_ = 'D:\\PUBG-Score-Board\\'

# for t in teams:
# 	print(t)
# 	mira, erang = heavy_splitter(path_, t)


	# data = []
	# for i in mira:
	# 	for x in i:
	# 			data.append(x)

	# miradf = pd.DataFrame(data)


	# miradf = miradf.groupby(['player', 'match_id', 'timeElapsed']).agg({'x':'mean', 'y':'mean'}).reset_index()


	# miradf = miradf[miradf['timeElapsed'] > 20]

t = 'circles_'

mapx, mapy = map_dimensions['Desert_Main']

mira_x, mira_y, erang_x, erang_y = split_(path_)

fig = plt.figure()
ax = plt.subplot()
img = plt.imread(path_ + map_path['Desert_Main'])
ax.imshow(img, extent=[0, mapx, mapy, 0])
# ax.scatter(miradf.x, miradf.y, c=miradf.match_id, s=5)
ax.hist2d(mira_x, mira_y, marker='o', c="red")
plt.show()
# fig.savefig(r'D:\PUBG-Score-Board\images\\' + t + 'miramar2.png', dpi=fig.dpi)

	# data = []
	# for i in erang:
	# 	for x in i:
	# 			data.append(x)

	# erangdf = pd.DataFrame(data)
	# erangdf = erangdf.groupby(['player', 'match_id', 'timeElapsed']).agg({'x':'mean', 'y':'mean'}).reset_index()
	# erangdf = erangdf[erangdf['timeElapsed'] > 20]

# mapx, mapy = map_dimensions['Baltic_Main']


# fig = plt.figure()
# ax = plt.subplot()
# img = plt.imread(path_ + map_path['Baltic_Main'])
# ax.imshow(img, extent=[0, mapx, mapy, 0])
# # ax.scatter(erangdf.x, erangdf.y, c=erangdf.match_id, s=5, label='rotation')
# ax.hist2d(erang_x, erang_y, c="red", marker='o', label='center')
# plt.show()
# fig.savefig(r'D:\PUBG-Score-Board\images\\' + t + 'erangal2.png', dpi=fig.dpi)