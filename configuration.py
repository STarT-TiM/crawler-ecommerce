import json

with open("config.json") as f:
	data = json.loads(f.read())

def getConfig():
	return data