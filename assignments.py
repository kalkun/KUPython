from KUPython import absalonSession
import re

class assignments(absalonSession): 
        """ assignments is a class to navigate to assignments folders of a given course 
            check status of handed in assignments 
            it inherites from the absalonSession class """
	
	def __init__(self, user, passw):

		# start absalon session
		absalonSession.__init__(self, user, passw)

    	# Get a list of coursefolders one from each course
		self.coursefolders = [self.coursefolder(courseID, navigate=False) for courseID in self.courses]

	def getassignmentsfolder(self, coursefolder):
		""" given a coursefolder getassignmentsfolder() returns the FolderID of the assignment folder """

		folderlist = re.findall('(?<=FolderID=)[0-9]+', coursefolder.text.encode('utf-8'))
		for ID in folderlist: 
			if len(self.getassignmentids(ID)) > 0: 
				return ID

	def getassignmentids(self, 
		FolderID): 
		""" Given a FolderID getassignmentids() returns a list of assignment IDs for the 
            assignments associated with the course that the folder belongs to. """	
		params = {'FolderID' : FolderID}
		overview = self.session.request("GET", "https://absalon.itslearning.com/Folder/processfolder.aspx", params=params)
        
		return re.findall('(?<=EssayID=)[0-9]+', overview.text.encode('utf-8'))

	def checkassignments(self,
		FolderID):
		""" given an assignment folder ID checkassignments returns a list of the assignments statuses """

		folderlist = self.getassignmentids(FolderID)
		# go through all EssayIDs in folderlist and collect status for each assignment
		# then puts the status into allStatus and returns the allStatus list of assignment statuses
		allStatus = []
		for assigns in folderlist:
			params = {'EssayID' : assigns}
			lookup = self.session.request("GET", "https://absalon.itslearning.com/essay/read_essay.aspx", params=params)
			status = re.search('(?<=<th>Status</th>\r\n\t\t\t\t).*?</td>', lookup.text.encode('utf-8'), flags=re.DOTALL)
			if status != None:
				allStatus.extend([status.group()])
		return allStatus
