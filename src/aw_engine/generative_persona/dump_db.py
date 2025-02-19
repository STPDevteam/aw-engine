import redis
import json

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Fetch all keys
keys = redis_client.keys('*')

# Create a dictionary to store key-value pairs
data = {}

# Iterate over keys and fetch values
for key in keys:

    # Fetch value corresponding to the key
    value = redis_client.hgetall(key)
    
    # Decode bytes to string if needed
    new_value = {}
    for key1, value1 in value.items():
        new_value[key1.decode('utf-8')] = value1.decode('utf-8')
    
    # Store key-value pair in dictionary
    data[key.decode('utf-8')] = new_value
    # print(new_value)


# Convert dictionary to JSON
json_data = json.dumps(data, indent=4)

# Print or save JSON data
print(json_data)
# If you want to save JSON data to a file
with open('redis_data.json', 'w') as json_file:
    json_file.write(json_data)
