
#Importing required modules
import http.client
import json
import time
import sys
import collections

#Parse user input to get API
api_key=sys.argv[1]

#Connection to http client
conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

#start from page 1
page_no=1
res_no=0
rcount=0

#Open file to write results down
f=open("movie_ID_name.csv","w")

#Keep incrementing page no till you get top 350 results (keep upper limit as 360 since page diplays 20 results)
while res_no<=360:

    #Getting data for movies with following paramters: Genre ID = 18 (Drama), primary_release_date=2014-01-01, sorted in descending order of popularity
    conn.request("GET", "/3/discover/movie?with_genres=18&primary_release_date.gte=2004-01-01&page={}&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key={}".format(page_no,api_key), payload)

    res = conn.getresponse()
    data = res.read()

    #Convert from json format to dict
    results=json.loads(data)

    #Write results to csv file
    for movie in results["results"]:
        if rcount<350:
            rcount+=1
            print("{},{}".format(movie["id"],movie["title"]))
        else:
            break

    #Increment page no and res_no
    page_no+=1
    res_no+=len(results["results"])

f.close()
