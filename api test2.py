#Used to make requests
import urllib.parse
import requests

api = 'http://www.omdbapi.com/?'
key = '&apikey=e0ad0310'

title = input("Enter film: ")
url = api + urllib.parse.urlencode({'t': title}) + key

data = requests.get(url).json()

filmTitle = data['Title']

for each in data:
    try:
        print(each + " = " + data[each])
    except:
        print(each)
        
