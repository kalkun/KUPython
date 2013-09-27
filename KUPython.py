

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
		courseID):
		""" Given a course ID coursefolder returns the course folder as a request.response object """
		
		#bind parameters
		params = {'CourseID' : courseID}

		# execute GET
		page = self.session.request('GET', "https://absalon.itslearning.com/main.aspx", params=params).text.encode('utf-8')

		#search for the course Folder ID and bind it to params
		params = { 'FolderID' : re.search('(?<=FolderID=)[0-9]+', page).group() }
		
		folder = self.session.request('GET', 'https://absalon.itslearning.com/Folder/processfolder.aspx', params)

		return folder

	def getassignmentsfolder(self, coursefolder):
		""" given a coursefolder getassignmentsfolder() returns the FolderID of the assignment folder """

		folderlist = re.findall('(?<=FolderID=)[0-9]+', coursefolder.text.encode('utf-8'))
		for ID in folderlist: 
			if len(self.getassignmentids(ID)) > 0: 
				return ID

	def getassignmentids(self, 
		FolderID): 
		"""	Given a FolderID getassignmentids() returns a list of assignment IDs for the 
			assignments associated with the course that the folder belongs to. """

		params = {'FolderID' : FolderID}
		overview = self.session.request("GET", "https://absalon.itslearning.com/Folder/processfolder.aspx", params=params)
		
		return re.findall('(?<=EssayID=)[0-9]+', overview.text.encode('utf-8'))

	def checkassignments(self,
		folderid):
		""" given an assignment folder checkassignments returns a list of the assignments statuses """

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

	def dump(page, responseobject=True, override=True, file='dump.html'):
		""" Dump page or text to a file
			the page parameter specifies what is to be written to the file
		 	if what is to be dumped is not a responseobject then pass responseobject=False 
		 	by default dump() writes to 'dump.html' pass any other filename to dump to another
		 	folder. 
		 	override can be set to False to not override what is already in file"""
		if override == True:
			dump = open('dump.html', 'w')
		else: 
			dump = open('dump.html', 'a')
		if responseobject == True:
			dump.write(page.text.encode('utf-8'))
		else:
			dump.write(page)
		dump.close()


