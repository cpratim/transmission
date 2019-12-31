import requests

base = 'http://127.0.0.1:5000'
folder = 'files'

def post_file(filename):
	with open(f'{folder}/{filename}', 'rb') as handle:
		requests.post(f'{base}/upload', files={filename: handle})

post_file('test1.jpg')