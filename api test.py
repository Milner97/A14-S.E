#Used to make requests
import urllib.request

search = 'http://www.omdbapi.com/?t='
title = input("Enter title of film: ")
search = search + title + "&apikey=e0ad0310"

#print(search)

x = urllib.request.urlopen(search)
print(x.read())

