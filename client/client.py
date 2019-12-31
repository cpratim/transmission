import requests
from time import sleep
import os
import json
from threading import Thread
from config import *

folder = FOLDER
base = BASE

def read_data(f):
	with open(f, 'r') as df:
		return json.loads(df.read())

def dump_data(f, d):
	with open(f, 'w') as df:
		json.dump(d, df, indent=4)

def compare(l1, l2):
	return (list(set(li1) - set(li2)))

def post_json(json):
	requests.post(f'{base}/update', json=json)

def post_file(filename):
	with open(f'{folder}/{filename}', 'rb') as handle:
		requests.post(f'{base}/upload', files={filename: handle})

def get_json():
	request = requests.get(f'{base}/files')
	return request.json()

def get_file(filename):
	req = requests.get(f'{base}/download/{filename}')
	with open(f'{folder}/{filename}', 'wb') as handle:
		handle.write(req.content)


print('Scanning for new Files')
def send():
	terminate = False
	data = read_data('files.json')
	change = False
	sleeptime = SLEEPTIME
	while not terminate:
		for file in os.listdir(folder):
			if file not in data['files']:
				print(f'New File Found: {file}')
				print(f'Uploading {file} to Server')
				post_file(file)
				print(f'{file} Successfully uploaded to Server')
				data['files'].append(file)
				change = True
		if change:
			dump_data('files.json', data)
			post_json(data)
			print('Data Posted to Web Server')
			data = read_data('files.json')
			change = False
		sleep(sleeptime)

def recieve():
	terminate = False
	data = read_data('files.json')
	change = False
	sleeptime = SLEEPTIME
	while not terminate:
		for file in get_json()['files']:
			if file not in data['files']:
				print(f'New File Found: {file} [Server Side]')
				print(f'Downloading {file} from Server')
				get_file(file)
				print(f'{file} Successfully Downloaded from Server')
				data['files'].append(file)
				change = True
		if change:
			dump_data('files.json', data)
			data = read_data('files.json')
			change = False
		sleep(sleeptime)

send_thread = Thread(target=send)
recieve_thread = Thread(target=recieve)
send_thread.start()
recieve_thread.start()