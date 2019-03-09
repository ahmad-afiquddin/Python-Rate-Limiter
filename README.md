# Python-Rate-Limiter

The rate limiter I have coded is an example of a leaky bucket implementation where at any given time, it would only allow 100 requests
on the server. After an hour has passed since the first request in the bucket has been made, if another request is made, the first request
will be popped from the bucket, and the newest request will be added to the end of the bucket. This ensures that there will be only 100
requests for any given hour. If another request is made, it will again check if the first request in the bucket has reached the one hour 
limit, and if yes, the first request is popped, and if no, the new request is rejected, and error 429 returned.

The implementation is memory intensive, as it will keep requests in the bucket, and pop them if necessary, but it is less processor intensive
as there are no periodic checks made to the bucket, as checks are only made once a new request is sent.

Files:
- settings.json contains settings for the rate limiter, tokens field specifies how many spaces are available in the bucket, and the time field
specifies the time each request is alive for
- ratelimiter.py is the main program that contains the necessary classes 
- tests.py is the test program that verifies the functionality of the rate limiter

ratelimiter.py:
Contains 4 classes, Request, Error429, User, and Server
- Request contains the time stamp the request was made, and a function that returns the time difference between current and time stamp.
request = Request() to make a request, and request.time_diff() to get time difference
- Error429 is for easy string returns. Call str(Error429(time until refresh))
- User contains the api key for the user, and the bucket that stores requests, and a function to make requests. user = User(api key) to initialize
and user.make_req() to make a request on the user.
- Server contains an {api key:User} dictionary that stores the User class for each api key, and handles requests from users. Initialize server 
with server = Server(), and initialize users for the server with server.user_init(api key). Users make request on the server with 
server.req_made(api key). 

tests.py:
After initializing 2 users with api keys user001 and user002, 6 test cases are run
- 1: Making a request on both users. Expecting success for both
- 2: Making 98 requests on both users. Expceting success for all requests.
- 3: Making the 100th request in the same hour. Expecting success.
- 4: Making a request after limit is reached. Expecting Error 429
- 5: Wait for time limit then make a new request. Expecting success since first tokens in both user buckets can be popped.
- 6: Making another request. Expecting Error 429 since first request tokens in both buckets have not expired.

Tests shows that there are no overlaps between users, and rate limiter is successful
