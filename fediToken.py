import requests, json, os, sys
from html.parser import HTMLParser

instance = input("what's your instance? don't include https:// prefix. eg; <sleepy.cafe>\n")
username = input("what's your user name?\n")
password = input("what's your password?\n")

class parseHTML(HTMLParser):
	inHeading = False
	token     = ""
	def handle_starttag(self, tag, attrs):
		print("start: ", tag)
		if tag == "br":
			self.inHeading = True
	def handle_endtag(self, tag):
		print("end: ", tag)
	def handle_data(self, data):
		print("data: ", data)
		if self.inHeading:
			self.token = data
			self.inHeading = False
		
parser = parseHTML()

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
	
def authenticate(inst, id, un, pw):
	data = [
	('authorization[scope][]', ''),
	('authorization[scope][]', 'read'),
	('authorization[scope][]', ''),
	('authorization[scope][]', 'write'),
	('authorization[name]', un),
	('authorization[password]', pw),
	('authorization[client_id]', id),
	('authorization[response_type]', 'code'),
	('authorization[redirect_uri]', 'urn:ietf:wg:oauth:2.0:oob'),
	('authorization[state]', ''),    ]
	
	response = requests.post("https://" + inst + "/oauth/authorize", data=data)
	parser.feed( response.content.decode("utf-8") )
	return parser.token
	
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

authentication = authenticate(instance, id, username, password)

accessToken = getToken(id, secret, authentication, instance)

while os.path.exists( os.path.join( sys.path[0], botName + ".txt" ) ):
	botName = input(botName + ".txt already exists,, pick a different file name punce\n")

with open( os.path.join(sys.path[0], botName + ".txt" ), "x" ) as f:
	f.write(accessToken)
	f.close
	
print( "access token " + accessToken + " written to " + botName + ".txt" )