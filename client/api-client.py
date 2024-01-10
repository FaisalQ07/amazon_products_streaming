import os
import linecache
import json
import glob
# Make sure that requests is installed in your WSL
import requests 

# We could just read the entire file, but if it's really big you could go line by line
# If you want make this an excercise and replace the process below by reading the whole file at once and going line by line

# Loop over the JSON file

print('here!')
for filepath in glob.iglob('../dataset/output/*.txt'):
    print(filepath)
    head, tail = os.path.split(filepath)
    filename = tail.split('.')[0]
    #set starting id and ending id
    start = 1
    end = 250
    i=start
    while i < end:
        line = linecache.getline(filepath, i)
        # print(line)
        # write the line to the API
        try:
            myjson = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in line {i}: {e}")
            # handle the error or skip the line if necessary
            continue
        print(myjson)
        if filename == 'amazon_products_small':
            response = requests.post('http://localhost:80/AmazonProduct', json=myjson)
        elif filename == 'amazon_categories':
            response = requests.post('http://localhost:80/Category', json=myjson)

        try:
            response_json = response.json()
            print(response_json)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in response: {e}")
        # increase i
        i+=1
