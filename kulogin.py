import requests
import re

s=requests.Session()

#cookie = dict(logondata='acc=1&lgn=tgw831')
params = { 	'username' : 'tgw831', 
			'password' : 'September2013', 
			'curl' : 'Z2F',
			'flags' : 0, 
			'forcedownlevel' : 0, 
			'formdir' : 6}
r = s.post("https://pabsws.ku.dk/CookieAuth.dll?Logon", data=params) #, cookies=cookie)

courseID1 = {'LocationID' : 49964, "LocationType" : 1, "FolderID" : 2062228}
#HCI = s.request("POST" ,"https://absalon.itslearning.com/ContentArea/ContentArea.aspx", params=courseID1)
#print HCI.url

Opgave5 = s.request('GET', 'https://absalon.itslearning.com/essay/read_essay.aspx?EssayID=2071783', data=params)

print Opgave5.text

#assignments = re.compile('EssayID=[0-9]+')

#print assignments.findall(HCI.text)

#print searchAssignments.group()

#print HCI.text

#essayID = {"EssayID" : 2071766}
#https://absalon.itslearning.com/essay/read_essay.aspx?EssayID=2071766