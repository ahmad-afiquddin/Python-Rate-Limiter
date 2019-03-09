#Importing modules
#For reading json formats
import json
#For time tracking
import time

#Reading from settings file
with open ('settings.json', encoding='utf-8') as settings_file:
    settings = json.loads(settings_file.read())

#Global settings
#In case someone tries to delibirately mess up the settings file
try:
    req_tokens = int(settings["tokens"])
    req_time = int(settings["time"])
#Exits program in case settings format is incorrect
except:
    print("Please make sure that only integers are used in the settings file")
    exit()

#Class for requests
class Request:
    def __init__(self):
	    #Timestamp for user request, since epoch
	    self.time_stamp = time.time()
	    #Time in readable format
	    self.time_read = time.asctime(time.localtime())

    def time_diff(self):
        return int(time.time() - self.time_stamp)

	#Return success message with time
    def __str__(self):
	    return "Successful request on " + self.time_read

#Class for Error
class Error429:
    def __init__(self, time_until):
	    self.time_until = time_until

    def __str__(self):
	    return ("Error 429! Rate limit exceeded. Try again in {} seconds".format(self.time_until))

#Class for user
class User():
    #Initializing user, records api_key and initializes a list of requests
    def __init__(self, api_key):
	    self.api_key = api_key
	    self.req_list = []

    def make_req(self):
	    if (len(self.req_list) < req_tokens):
	    	#Making a new request and apending it to list
		    self.req_list.append(Request())
		    #Returns success message
		    return str(self.req_list[-1])

        #If request limit has been reached
	    if (len(self.req_list) >= req_tokens):
            #Check if first request in list has gone over time limit
		    if (self.req_list[0].time_diff() > req_time):
                #Remove said request, and add a new request
			    self.req_list.pop(0)
			    self.req_list.append(Request())
                #Return success message
			    return str(self.req_list[-1])
		    else:
                #Return error429
			    return str(Error429(req_time - self.req_list[0].time_diff()))

    #Return info for user
    def __str__(self):
        first_token = self.req_list[0].time_diff()
        last_token = self.req_list[-1].time_diff()
        return ("{} Earliest request in bucket was made {} seconds ago, most recent request was made {} seconds ago. A total of {} requests were made".format(self.api_key, first_token, last_token, len(self.req_list)))

#Class for server
class Server:
    #Initialize {api_key:User} dictionary
    def __init__(self):
        self.user_dict = {}

    def user_init(self, api_key):
        if (not self.user_dict.get(api_key)):
            self.user_dict.update({api_key:User(api_key)})
        else:
            return ("User with api key {} already exists".format(api_key))

    def req_made(self, api_key):
        return self.user_dict.get(api_key).make_req()

    def get_user(self, api_key):
        if (self.user_dict.get(api_key)):
            return self.user_dict.get(api_key)
        else:
            return ("User with api key {} does not exist".format(api_key))







