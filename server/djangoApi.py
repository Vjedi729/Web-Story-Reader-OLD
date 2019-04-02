#import MySQLdb

# Look at Django and Flask
# Comes in two parts: Connect to a Database and Send/Receive HTTP


select_username = "webstoryreader_guest"
select_password = "abcdefghijklmnopqrstuvwxyz123456789"
def runSelect(query_string):
    #conn = MySQLdb.connect(host="localhost", user=username, passwd=password)
    #cursor = conn.cursor()
    #cursor.execute(query_string)
    return "Did not run select query: <<" + query_string + ">>"

def runQuery(query_string):
    return "Did not run query: <<" + query_string + ">>"


#######################
#     HTTP STUFF
#######################

def makeHttpResponse(status, content_type, content): # You can add inputs, but they have to have defaults
    # TODO: FIX THIS
    return "HTTP/1.1 "+status+"\nContent-Type: "+content_type+"\n"+content
