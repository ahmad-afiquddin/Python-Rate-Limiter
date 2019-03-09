#Tests the functionality of the python-based rate limiter
#settings.json currently set to limit a user to 100 requests per hour


#Import server class from ratelimiter.py
from ratelimiter import Server
#For reading json formats
import json
#Import time module
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



#Initialize testing server
test_server = Server()

#Api keys for users
user1 = "user001"
user2 = "user002"

#Initialize 3 users on server with 3 unique api keys
#User 1
print("Initializing 2 users with api_keys: user001, user002")
test_server.user_init(user1)
test_server.user_init(user2)

print("\nTest case #1: Making a request on user001 and user002")
#Expected: Success on all requests
#Make a request each on all users
print("Making a request on user001")
print(test_server.req_made(user1))
print("Making a request on user002")
print(test_server.req_made(user2))
time.sleep(req_time/500)

print("\nTest case #2: Adding {} requests to both users".format(req_tokens - 2))
#Making another token limit - 2 requests
#Expected: Success on all requests
for ind in range(req_tokens - 3):
    test_server.req_made(user1)
    test_server.req_made(user2)
    time.sleep(req_time/500)

print("Most recent requests:")
print(test_server.req_made(user1))
print(test_server.req_made(user2))
time.sleep(req_time/500)


#Printing user info
print("User infos:")
print(test_server.get_user(user1))
print(test_server.get_user(user2))


print("\nTest case #3: Making last allowable request within set period")
#Expected: Success on all requests
print("Making a request on user001")
print(test_server.req_made(user1))
print("Making a request on user002")
print(test_server.req_made(user2))
time.sleep(req_time/500)


print("\nTest case #4: Making a request after limit has been reached")
#Expected: Error 429 on all requests
print("Making a request on user001")
print(test_server.req_made(user1))
print("Making a request on user002")
print(test_server.req_made(user2))
time.sleep(req_time/500)

time.sleep(req_time)
print("\nTest case #5: Making a request after time limit has passed")
#Expected: Success on all requests
print("Making a request on user001")
print(test_server.req_made(user1))
print("Making a request on user002")
print(test_server.req_made(user2))
time.sleep(req_time/1000)

print("\nTest case #6: Making another request")
#Expected: Error 429 on all requests
print("Making a request on user001")
print(test_server.req_made(user1))
print("Making a request on user002")
print(test_server.req_made(user2))




