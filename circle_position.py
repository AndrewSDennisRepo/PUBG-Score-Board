

import json

path = r'D:\PUBG-Score-Board\2021\2b8a154a-be17-4137-b02e-4f4a48976fbd.json'



with open(path, 'r')  as f:
	file = json.loads(f.read())



for x in file['telemetry']:
	try:
		print(x['gameState'])
	except:
		pass