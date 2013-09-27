#########################################################################
#                                                                       #
#   KUPython is a module intended to help building                      #
#   applications for KU's Absalon in Python                             #
#                                                                       #
#   In order for KUPython to work Requests need to be                   #
#   installed.                                                          #
#                                                                       #
#   link to install Requests:                                           #
#   http://docs.python-requests.org/en/latest/user/installed            #
#                                                                       #
#                                                                       #
#                                                                       #
#                                                                       #
#########################################################################

import requests
import re


class absalonSession:
	""" A class to begin a user session on KU's studentnet Absalon 
		as well as providing some basic navigation on the site	"""

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
			'forcedownlevel' : forcedownlevel,
			'formdir' : formdir
		}

		# assign a request session object to self
		self.session = requests.Session()

		# start user session
		tmp = self.session.post("https://pabsws.ku.dk/CookieAuth.dll?Logon", data=self.params)

		# self.courses is a list of course IDS for the current user
		self.courses = re.findall('(?<=CourseID=)[0-9]+', tmp.text.encode('utf-8'))

	def coursefolder(self, 
		courseID, navigate=True):
		""" Given a course ID coursefolder returns the course folder as a request.response object 
			by default. Returns the Folder ID if navigate is set to False"""
		
		#bind parameters
		params = {'CourseID' : courseID}

		# execute GET
		page = self.session.request('GET', "https://absalon.itslearning.com/main.aspx", params=params).text.encode('utf-8')

		#search for the course Folder ID 
		folderID = re.search('(?<=FolderID=)[0-9]+', page).group()
		if navigate == False: 
			return folderID	

		else: 
			# and bind it to params
			params = { 'FolderID' : folderID }
			folder = self.session.request('GET', 'https://absalon.itslearning.com/Folder/processfolder.aspx', params)

			return folder

	def dump(page, responseobject=True, override=True, file='dump.html'):
		""" Dump page or text to a file
            the page parameter specifies what is to be written to the file
            if what is to be dumped is not a responseobject then pass responseobject=False 
            by default dump() writes to 'dump.html' pass any other filename to dump to another
            folder. 
            override can be set to False to not override what is already in file """
		if override == True:
			dump = open('dump.html', 'w')
		else: 
			dump = open('dump.html', 'a')
		if responseobject == True:
			dump.write(page.text.encode('utf-8'))
		else:
			dump.write(page)
		dump.close()