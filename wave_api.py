import requests
import pprint
import json
import os

url = 'https://login.salesforce.com/services/oauth2/token'
d = {
	'client_id': '3MVG91ftikjGaMd9IQ9dEbGephypa2HaVfYpdeXiGBSuXeEmhDH4QWvFhR.aDj0.q1ZPPLxzTzWNfbCmS8fso',
 	'client_secret': '6723928713317818058',
 	'grant_type': 'password',
 	'password': os.environ['SFDC_PWD_ANALYTICS'],
 	'username': os.environ['SFDC_USR_ANALYTICS']
}

print('Contacting SF\n')

r = requests.post(url, data=d)
print ('\n')
pprint.pprint (r.json())
print ('\n')

h = { 'Authorization': 'Bearer ' + r.json()['access_token']}
base_url = r.json()['instance_url']+'/services/data/v34.0/wave'

r2 = requests.get(base_url, headers=h)
print ('\n')
pprint.pprint(r2.json())
print ('\n')

q = "q = load \"0Fb150000004CA4CAM/0Fc150000004CDpCAM\";"
q = q + "q = group q by 'Suburb';"
q = q + "q = foreach q generate 'Suburb' as 'Suburbs', sum('Occurrences') as 'Occurrences';"
q = q + "q = limit q 1000;"
query = {'query': q}

query_url = base_url + '/query'

h_json = h.copy()
h_json['Content-Type'] = 'application/json'

r3 = requests.post(query_url, headers=h_json, data=json.dumps(query))

pprint.pprint(r3.json())
