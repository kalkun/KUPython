#################################################################
#																#
#	KUPython is a module intended to help building				#
#	applications for KU's Absalon in Python 					#
#																#
#	In order for KUPython to work Requests need to be 			#
#	installed. 													#
#																#
#	link to install Requests:									#
#	http://docs.python-requests.org/en/latest/user/installed 	#
#																#
#																#
#																#
#																#
#################################################################

from requests import Session


class absalonSession:
	""" A class to begin a user session on KU's studentnet Absalon """
	def __init__(self, 
		username, 
		password, 
		curl = 'Z2F', 
		flags = 0, 
		forcedownlevel = 0, 
		formdir = 6):
		
		# assign parameters to POST to server
		self.params = {	
			'username' : username, 
			'password' : password, 
			'curl' : curl,
			'flags' : flags,
			'forcedownlevel' : forcedownlevel
			'formdir' : formdir
		}

		# assign a request session object to self
		self.session = requests.Session()

	def login(self):
		return self.session.post("https://pabsws.ku.dk/CookieAuth.dll?Logon", data=params)
