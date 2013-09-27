#########################################################################
#                                                                       #
#	KUPython is a module intended to help building                      #
#	applications for KU's Absalon in Python                             #
#                                                                       #
#	In order for KUPython to work Requests need to be                   #
#	installed.                                                          #
#                                                                       #
#	link to install Requests:                                           #
#	http://docs.python-requests.org/en/latest/user/installed            #
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

		self.coursefolders = {}

	def coursefolder(self, 
		courseID):
		# go to course page of a given courseID
		
		#bind parameters
		params = {'CourseID' : courseID}

		# execute GET
		page = self.session.request('GET', "https://absalon.itslearning.com/main.aspx", params=params).text.encode('utf-8')

		#search for the course Folder ID and bind it to params
		params = { 'FolderID' : re.search('(?<=FolderID=)[0-9]+', page).group() }
		
		folder = self.session.request('GET', 'https://absalon.itslearning.com/Folder/processfolder.aspx', params)

		return folder

	def getassignmentsfolder(self, coursefolder):
		# given a coursefolder it finds the assignment folder in it
		return None

	def getassignmentids(self, 
		FolderID): 
		# Given a FolderID getassignmentids looks up EssayID which is essentially to get 
		# pages of each specific assignment for the course. 

		params = {'FolderID' : FolderID}
		overview = self.session.request("GET", "https://absalon.itslearning.com/Folder/processfolder.aspx", params=params)
		
		return re.findall('(?<=EssayID=)[0-9]+', overview.text.encode('utf-8'))

	def checkassignments(self,
		folderid):
		# given an assignment folder it checks all the assignment pages to check their status

		folderlist = self.getassignmentids(folderid)
		allStatus = []
		for assigns in folderlist:
			params = {'EssayID' : assigns}
			lookup = self.session.request("GET", "https://absalon.itslearning.com/essay/read_essay.aspx", params=params)
			status = re.search('(?<=<th>Status</th>\r\n\t\t\t\t).*?</td>', lookup.text.encode('utf-8'), flags=re.DOTALL)
			if status != None:
				allStatus.extend([status.group()])
			#status = re.search('(?<=<th>Status</th>)^<td>$</td>', check)
		return allStatus



