import os
import json

def dump_data(f, d):
	with open(f, 'w') as df:
		json.dump(d, df, indent=4)

for file in os.listdir('server'):
	os.remove(f'server/{file}')
for file in os.listdir('files'):
	os.remove(f'files/{file}')
for file in os.listdir('recieve'):
	os.remove(f'recieve/{file}')

dump_data('server.json', {'files': []})
dump_data('files.json', {'files': []})
dump_data('recieve.json', {'files': []})
print('Reset Complete')