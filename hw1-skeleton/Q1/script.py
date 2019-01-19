
#Importing required modules
import http.client
import json
import time
import sys
import collections

#Start timer
st = time.time()

#Parse user input to get API
api_key=sys.argv[1]

#Connection to http client
conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

######----------------------------------------------------------------------------------------------------------------######
######-------------------------------------------------- PART 1.1.b --------------------------------------------------######
######----------------------------------------------------------------------------------------------------------------######
#Desc: retrieve 350 most popular movies from Drama genre released in 2004 or after

#start from page 1, initialise counters at 0
page_no=1
res_no=0
rcount=0

#Initialise dict to store movie id and movie title (for part c)
movies_dict={}

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
            f.write("{},{}\n".format(movie["id"],movie["title"]))
            movies_dict[movie["id"]]=movie["title"]
        else:
            break

    #Increment page no and res_no
    page_no+=1
    res_no+=len(results["results"])

f.close()


######----------------------------------------------------------------------------------------------------------------######
######-------------------------------------------------- PART 1.1.c --------------------------------------------------######
######----------------------------------------------------------------------------------------------------------------######
#Desc: Retrieve 5 similar movies for each of the movies in part 1.1.b

#Initialise a set which stores similar movies
s_movies_set=set()

#Initialise query counter (starts at 20 since 19 queries have already been made for 1.1.b). Once 40 queries are done, sleep for 10 seconds
q_count=20

#Loop through each movie in movies_dict
for id in movies_dict:

    q_count+=1
    conn.request("GET", "/3/movie/{}/similar?page=1&language=en-US&api_key={}".format(id,api_key), payload)

    res = conn.getresponse()
    data = res.read()

    #Convert from json format to dict
    results=json.loads(data)

    #Initialise s_count to store first 5 results only
    s_count=0

    for movie in results["results"]:
        if s_count<5:
            s_count+=1
            row="{},{}".format(min(movies_dict[id],movie["title"]),max(movies_dict[id],movie["title"]))
            s_movies_set.add(row)
        else:
            break

    #If 40 queries are done, refresh query counter and sleep for 10 secs
    if q_count>=40:
        q_count=1
        time.sleep(10)

#Sort and store list of movies
s_movies_list=sorted(list(s_movies_set))

#Open file for similar movies
with open("movie_ID_sim_movie_ID.csv","w") as f:
    for entry in s_movies_list:
        f.write("{}\n".format(entry))

#Print elapsed time
#print("Time elapsed: {}".format(time.time()-st))
