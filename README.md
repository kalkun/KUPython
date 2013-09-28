#########################################################################
#                                                                       #
#   KUPython                                                            #
#                                                                       #
#########################################################################
KUPython is a small Python module intended to help easily build scripts or small 
applications for KU's studentnet Absalon.

In order for KUPython to work the [Requests Library](http://docs.python-requests.org/en/latest/user/install/) need to be installed.

#########################################################################

- Get started: 
    - Start a new session with the absalonSession class. Example:
      
            from KUPython import absalonSession
            from assignments import assignments
            
            user = <username>
            passw = <password>
            
            kusession = absalonSession(user, passw)

- Test status for assignments.
  - Example to test for assignments from all courses

            def getstatus():
                newsession = assignments(user, passw)
            
                status = "" 
                for folder in newsession.assignmentfolders:
                    status += newsession.checkassignments(folder)
                return status
      
    - Since the result from getstatus will be html formatted it can just be dumped to a file. 
  
            def dump(html):
                dump = open('result.html', 'w')
                dump.write(html)
                dump.close()


