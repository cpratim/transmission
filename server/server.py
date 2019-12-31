from flask import Flask, send_file, request, jsonify
import os
import json

def read_data(f):
	with open(f, 'r') as df:
		return json.loads(df.read())

def dump_data(f, d):
	with open(f, 'w') as df:
		json.dump(d, df, indent=4)

app = Flask(__name__)

@app.route('/')
def index():
	return 'Transmission Server Running'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	req = request.files
	filename = [key for key in req][0]
	print(f'Recieved File {filename}')
	req[filename].save(f'storage/{filename}')
	return ""

@app.route('/update', methods=['GET', 'POST'])
def update():
	data = request.get_json()
	dump_data('server.json', data)
	print(read_data('server.json'))
	return ""

@app.route('/files')
def files():
	return jsonify(read_data('server.json'))

@app.route('/download/<string:file>')
def download(file):
	return send_file(f'storage/{file}')

if __name__ == '__main__':
	app.run()