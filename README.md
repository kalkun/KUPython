#########################################################################
#                                                                       #
#   KUPython                                                            #
#                                                                       #
#########################################################################
KUPython is a Python module intended to help building applications 
for KU's studentnet Absalon.

In order for KUPython to work Requests need to be installed.

link to install Requests:                                           
<http://docs.python-requests.org/en/latest/user/install/>

#########################################################################

- Get started: 
  > Start a new session with the absalonSession class. Example:
    
      from KUPython import absalonSession, assignments
      
      user = <username>
      passw = <password>
      
      kusession = absalonSession(user, passw)

- Test status for assigments.
  > Example to test for assignments from all courses

      def getstatus():
          newsession = assignments.assignment(user, passw)
        
          result = "" 
          for folder in newsession.assignmentfolders:
              result += assigns.checkassignments(folder)
          return result
      
  > Since the result from getstatus will be html formatted it can just be dumped to a file. 
  
    def dump(html)
        dump = open('result.html', 'w')
        dump.write(html)
        dump.close()


