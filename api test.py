#Used to make requests
import urllib.request

#gets user to enter title of film
title = input("Enter title of film: ")

#used to allow multiple word titles
title = title.replace(" ", "+")

#adds title to a search url
search = 'http://www.omdbapi.com/?t=' + title + "&apikey=e0ad0310"

#Request data from API and print
jsontext = urllib.request.urlopen(search)
jt = jsontext.read()
print(jt)

