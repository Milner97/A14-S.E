#Software Engineering Program - Group A14
from tkinter import*
import urllib.parse
import requests

class MovieDBApplication(Frame):
    def __init__(self, master):
        #Frame properties
        super(MovieDBApplication, self).__init__(master)

        #Create frame
        self.SelectUserFrame = Frame(self)
        self.ResultsFrame = Frame(self)
        self.WishlistFrame = Frame(self)

        #Put widgets in frame
        self.CreateResultsWidgets(filmInfo)
        

        #Set up selct user frame
        self.SearchFrame = Frame(self)
        #root.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
        root.title("ACME Movie DataBase")
        ScWi = self.SearchFrame.winfo_screenwidth()
        #LabelToCentre = Label(self.SearchFrame)
        #LabelToCentre.grid(row = 0, column = 0, padx = (ScWi - 550)/4, pady = 30)
        LogoLabel = Label(self.SearchFrame, text = "ACME Movie Database", fg = "black", font = ("Arial", 30, "bold"))
        LogoLabel.grid(row = 1, column = 1, columnspan = 3, pady = 10, padx = 10)        
        SearchLabel = Label(self.SearchFrame, text = "Search Films:", font = ("Arial", 12, "bold"))
        SearchLabel.grid(row = 2, column = 1)
        SearchEntry = Entry(self.SearchFrame, font = ("Arial", 12))
        SearchEntry.grid(row = 2, column = 2, padx = 10)
        GoButton = Button(self.SearchFrame, text = "Go", font = ("Arial", 12, "bold"), command = lambda:self.SearchFilm(SearchEntry))
        GoButton.grid(row = 2, column = 3)
        self.SearchFrame.grid()


    def SearchFilm(self, SearchEntry):
        #Get data from the api
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

        #Set display to use for textvariable meaning it can change when reopened
        display.set(filmInfo)
        #Display in results frame
        InfoLabel = Label(self.ResultsFrame, textvariable = display, font = ("Arial", 12))
        InfoLabel.grid(row = 2, column = 1, columnspan = 3, padx = 5)
        #Clear search bar
        SearchEntry.delete(0,END)
        self.SearchFrame.grid_remove()
        self.ResultsFrame.grid()
        
    #Create Results frame widgets
    def CreateResultsWidgets(self, filmInfo):
        ResTitleLabel = Label(self.ResultsFrame, text = "ACME Movie Database", font = ("Arial", 30, "bold"))
        ResTitleLabel.grid(row = 1, column = 1, columnspan = 3, pady = 10)
        BackButton = Button(self.ResultsFrame, text = "Back", font = ("Arial",12, "bold"), command = lambda:self.BackToSearch())
        BackButton.grid(row = 3, column = 2)

    #removes results frame and displays search frame
    def BackToSearch(self):
        self.ResultsFrame.grid_remove()
        self.SearchFrame.grid()
        
        


#Main
root = Tk()
filmInfo = StringVar()
display = StringVar()
MovieDBApplication(root).grid()
root.mainloop()
