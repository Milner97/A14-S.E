#Software Engineering Program - Group A14
from tkinter import*
import urllib.parse
import requests
import re
import sqlite3
from tkinter.messagebox import *


def createDB(cur):
    conn = sqlite3.connect('Wishlist.db')
    cur = conn.cursor()
    try:
        #Create wishlist db table
        cur.execute("CREATE TABLE if not exists Wishlist(imdbID VARCHAR(9) PRIMARY KEY, Title VARCHAR(50), Director VARCHAR(20), Cast VARCHAR(100), Plot VARCHAR(200), Release VARCHAR(15), AllInfo VARCHAR(500))")
    except:
        showerror("Error creating Wishlist")

    

class MovieDBApplication(Frame):
    def __init__(self, master):
        #Frame properties
        super(MovieDBApplication, self).__init__(master)

        #Create frame
        self.SelectUserFrame = Frame(self)
        self.ResultsFrame = Frame(self)
        self.AllInfoFrame = Frame(self)

        #Put widgets in frame
        self.CreateResultsWidgets()
        self.CreateMoreInfoWidgets()
        

        #Set up selct user frame
        self.SearchFrame = Frame(self)
        root.title("ACME Movie DataBase")
        LogoLabel = Label(self.SearchFrame, text = "ACME Movie Database", font = ("Arial", 20, "bold"))
        LogoLabel.grid(row = 1, column = 1, columnspan = 4, pady = 10, padx = 10)        
        SearchLabel = Label(self.SearchFrame, text = "Search Films:")
        SearchLabel.grid(row = 2, column = 1)
        SearchEntry = Entry(self.SearchFrame)
        SearchEntry.grid(row = 2, column = 2, padx = 10)
        SAPI.set("Search API 1")
        SearchAPI = OptionMenu(self.SearchFrame, SAPI, "Search API 1", "Search API 2")
        SearchAPI.grid(row = 2, column = 3)
        GoButton = Button(self.SearchFrame, text = "Go",command = lambda:self.SearchFilm(SearchEntry))
        GoButton.grid(row = 2, column = 4)
        WishlistButton = Button(self.SearchFrame, text = "WishList", command = lambda:self.SearchToWishlist())
        WishlistButton.grid(row = 3, column = 2, pady = 5)
        self.SearchFrame.grid()


    def SearchFilm(self, SearchEntry):
        if SAPI.get() == "Search API 1":
            #Get data from the omdb api
            api = 'http://www.omdbapi.com/?'
            key = '&apikey=e0ad0310'
            url = api + urllib.parse.urlencode({'t': SearchEntry.get()}) + key
            data = requests.get(url).json()

            #Put data into a readable string with line spaces
            filmInfo = ""
            for each in data:
                try:
                    filmInfo = filmInfo + str(each + ": " + data[each]) + "\n"
                except:
                    pass

            #Set displays to use for textvariable meaning it can change when reopened
            TitleDisplay.set("N/A")
            DirectorDisplay.set("N/A")
            CastDisplay.set("N/A")
            PlotDisplay.set("N/A")
            ReleaseDisplay.set("N/A")
            fi = re.split(': |\n', filmInfo)
            for i in range(0, len(fi)):
                if fi[i] == "imdbID":
                    ID.set(fi[i+1])
                if fi[i] == "Title":
                    TitleDisplay.set(fi[i+1])
                if fi[i] == "Director":
                    DirectorDisplay.set(fi[i+1])
                if fi[i] == "Actors":
                    CastDisplay.set(fi[i+1])
                if fi[i] == "Plot":
                    PlotDisplay.set(fi[i+1])
                if fi[i] == "Released":
                    ReleaseDisplay.set(fi[i+1])
                if fi[i] == "Error":
                    ErrorDisplay.set("Error: " + fi[i+1])
                AllDisplay.set(filmInfo) 

        else:
            #get data from the movie database api
            api = 'https://api.themoviedb.org/3/search/movie?api_key=f6842cb02901b733ae86df5f65bd1842&'
            url = api + urllib.parse.urlencode({'query': SearchEntry.get()})
            data = requests.get(url).json()

            #Set displays to use for textvariable meaning it can change when reopened
            TitleDisplay.set("N/A")
            DirectorDisplay.set("N/A")
            CastDisplay.set("N/A")
            PlotDisplay.set("N/A")
            ReleaseDisplay.set("N/A")
            ErrorDisplay.set("")

            #FIX
            #if data['results']['total_results'] == 0:
            #    ErrorDisplay.set("Error: No film found")
            if 1 == 2:
                pass

            else:            
                data = data['results'][0]

                #Put data into a readable string with line spaces
                filmInfo = ""
                for each in data:
                    try:
                        filmInfo = filmInfo + str(each + ": " + data[each]) + "\n"
                    except:
                        pass

                fi = re.split(': |\n', filmInfo)
                for i in range(0, len(fi)):
                    if fi[i] == "imdbID":
                        ID.set(fi[i+1])
                    if fi[i] == "title":
                        TitleDisplay.set(fi[i+1])
                    if fi[i] == "overview":
                        PlotDisplay.set(fi[i+1])
                    if fi[i] == "release_date":
                        ReleaseDisplay.set(fi[i+1])
                    if fi[i] == "Error":
                        ErrorDisplay.set("Error: " + fi[i+1])
                    AllDisplay.set(filmInfo)
                print(fi)

        #Display in results frame
        TitleLabel2 = Label(self.ResultsFrame, textvariable = TitleDisplay)
        TitleLabel2.grid(row = 2, column = 2)
        DirectorLabel2 = Label(self.ResultsFrame, textvariable = DirectorDisplay)
        DirectorLabel2.grid(row = 3, column = 2)
        CastLabel2 = Label(self.ResultsFrame, textvariable = CastDisplay)
        CastLabel2.grid(row = 4, column = 2)
        PlotLabel2 = Label(self.ResultsFrame, textvariable = PlotDisplay)
        PlotLabel2.grid(row = 5, column = 2)
        ReleaseLabel2 = Label(self.ResultsFrame, textvariable = ReleaseDisplay)
        ReleaseLabel2.grid(row = 6, column = 2)
        ErrorLabel = Label(self.ResultsFrame, textvariable = ErrorDisplay)
        ErrorLabel.grid(row = 7, column = 1, columnspan = 2)
        MoreButton = Button(self.ResultsFrame, text = "More Info", command = lambda:self.MoreInfo(filmInfo))
        MoreButton.grid(row = 8, column = 3, padx = 5)
        WishListButton = Button(self.ResultsFrame, text = "Add to Wishlist", command = lambda:self.AddToWishlist(cur))
        WishListButton.grid(row = 8, column = 2, pady = 5)

        #grid results frame, remove search frame
        self.SearchFrame.grid_remove()
        self.ResultsFrame.grid()
        
        #Clear search bar
        SearchEntry.delete(0,END)
        
        
    #Create Results frame widgets
    def CreateResultsWidgets(self):
        LogoLabel = Label(self.ResultsFrame, text = "ACME Movie Database", font = ("Arial", 20, "bold"))
        LogoLabel.grid(row = 1, column = 1, columnspan = 3, pady = 10)
        TitleLabel = Label(self.ResultsFrame, text = "Title:")
        TitleLabel.grid(row = 2, column = 1)
        DirectorLabel = Label(self.ResultsFrame, text = "Director:")
        DirectorLabel.grid(row = 3, column = 1)
        CastLabel = Label(self.ResultsFrame, text = "Cast:")
        CastLabel.grid(row = 4, column = 1)
        PlotLabel = Label(self.ResultsFrame, text = "Plot:")
        PlotLabel.grid(row = 5, column = 1)
        ReleaseLabel = Label(self.ResultsFrame, text = "Release Date:")
        ReleaseLabel.grid(row = 6, column = 1)
        BackButton = Button(self.ResultsFrame, text = "Back", command = lambda:self.BackToSearch())
        BackButton.grid(row = 8, column = 1)

    def CreateMoreInfoWidgets(self):
        LogoLabel = Label(self.AllInfoFrame, text = "ACME Movie Database", font = ("Arial", 20, "bold"))
        LogoLabel.grid(row = 1, column = 1, pady = 10)
        BackButton = Button(self.AllInfoFrame, text = "Back", command = lambda:self.MoreInfoToResults())
        BackButton.grid(row = 3, column = 1)
        

    #removes results frame and displays search frame
    def BackToSearch(self):
        self.ResultsFrame.grid_remove()
        self.SearchFrame.grid()
        ErrorDisplay.set("")
        ID.set("")

    def MoreInfo(self, filmInfo):
        AllLabel = Label(self.AllInfoFrame, textvariable = AllDisplay)
        AllLabel.grid(row = 2, column = 1)
        self.ResultsFrame.grid_remove()
        self.AllInfoFrame.grid()

    def MoreInfoToResults(self):
        self.AllInfoFrame.grid_remove()
        self.ResultsFrame.grid()

    def SearchToWishlist(self):
        #Open new scroll window for wishlist. Code adapted from https://www.tutorialspoint.com/python/tk_scrollbar.htm
        Wishlist = Toplevel(root)
        Wishlist.title("Wishlist")
        scrollbar = Scrollbar(Wishlist)
        scrollbar.pack(side = RIGHT, fill = Y)
        WL = Listbox(Wishlist, yscrollcommand = scrollbar.set, font = ("Arial", 12))

        #Get titles from wishlist database
        cur.execute('SELECT Title FROM Wishlist')
        data = cur.fetchall()
        for title in data:
            print(title)
            title2 = ""
            for character in title:
                if character != "{" and character != "}":
                    title2 = title2 + character
            title = title2
            WL.insert(END, title)
        WL.pack(side = LEFT, fill = BOTH)
        scrollbar.config(command = WL.yview)

    def AddToWishlist(self,cur):
        #error note if movie is not found
        if ID.get() == "":
            showerror("Error", "Movie not found, cannot add to wishlist")
        #Get data 
        else:
            imdbID = ID.get()
            T = TitleDisplay.get()
            D = DirectorDisplay.get()
            C = CastDisplay.get()
            P = PlotDisplay.get()
            R = ReleaseDisplay.get()
            A = AllDisplay.get()
            WishlistDetails = (imdbID, T, D, C, P, R, A)
            #Add data to database
            try:
                cur.execute("INSERT INTO Wishlist(imdbID, Title, Director, Cast, Plot, Release, AllInfo) "+\
                            "Values (?,?,?,?,?,?,?)", WishlistDetails)
                conn.commit()
                showinfo("Wishlist", "Movie added to wishlist")
            except sqlite3.Error as e:
                showerror("Error", "Movie already in Wishlist")
    

        
#Main
root = Tk()

#set up database
filename = "Wishlist.db"
try:
    with open(filename) as f:("testing file exists")
except:
    pass

#Connect to database, if not exists then creates
conn = sqlite3.connect('Wishlist.db')

#Set up cursor, interfaces between program and database
cur = conn.cursor()
createDB(cur)

filmInfo = StringVar()
ID = StringVar()
TitleDisplay = StringVar()
DirectorDisplay = StringVar()
CastDisplay = StringVar()
PlotDisplay = StringVar()
ReleaseDisplay = StringVar()
ErrorDisplay = StringVar()
AllDisplay = StringVar()

SAPI = StringVar()


MovieDBApplication(root).grid()
root.mainloop()
conn.close()
