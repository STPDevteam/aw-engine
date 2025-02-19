import redis

# create a connection to the Redis server
r = redis.Redis(host='localhost', port=1234, db=0)

# set a hash with multiple fields
r.hmset("user:1001", {"name": "John", "email": "john@example.com", "age": 25})

# get all fields and values of the hash
user_data = r.hgetall("user:1001")

# print the user data
print(user_data)