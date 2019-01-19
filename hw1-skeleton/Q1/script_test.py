
#Importing required modules
import http.client
import json
import time
import sys
import collections

#Parse user input to get API
api_key=sys.argv[1]

#Add api key to query
api_query="dwjnc"

print(api_key,api_query)

#Connection to http client
conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

#Getting data for movies with following paramters: Genre ID = 18 (Drama), primary_release_date=2014-01-01, sorted in descending order of popularity
conn.request("GET", "/3/discover/movie?with_genres=18&primary_release_date.gte=2004-01-01&page=1&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key={}".format("e24ed11741debeb8dbf62f84b0adc8dd"), payload)

res = conn.getresponse()
data = res.read()
