import requests, json, os, sys
from webbrowser import open as openBrowser

instance = input("what's your instance? don't include https:// prefix. eg; <sleepy.cafe>\n")

def getClientID(inst, name):

	data = {
	'baseurl'      : inst,
	'client_name'  : name,
	'redirect_uris': 'urn:ietf:wg:oauth:2.0:oob',
	'scopes'       : 'read write',
	'website'      : ''    }

	response = requests.post('https://' + inst + '/api/v1/apps', data=data)
	response = json.loads(response.content)
	return [ response["client_id"], response["client_secret"]    ]
	
def getToken(id, sec, code, inst):
	files = {
	'grant_type'   : (None, 'authorization_code'),
	'redirect_uri' : (None, 'urn:ietf:wg:oauth:2.0:oob'),
	'client_id'    : (None, id),
	'client_secret': (None, sec),
	'code'         : (None, code),    }
	
	response = requests.post( "https://" + inst + "/oauth/token", files=files )
	response = json.loads( response.content )
	return response["access_token"]

botName = input("name your bot:\n")
	
stuff  = getClientID(instance, botName)
id     = stuff[0]
secret = stuff[1]

userInput = input("press enter to open your default web browser. click accept and paste the code that appears here.")

openBrowser( "https://" + instance + "/oauth/authorize?client_id=" + id + "&redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=code&scope=read+write" )

code      = input()

token = getToken(id, secret, code, instance)

while os.path.exists( os.path.join( sys.path[0], botName + ".txt" ) ):
	botName = input(botName + ".txt already exists,, pick a different file name punce\n")

with open( os.path.join(sys.path[0], botName + ".txt" ), "x" ) as f:
	f.write(token)
	f.close
	
print( "access token " + token + " written to " + botName + ".txt" )