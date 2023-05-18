#import tk library
from tkinter import *  
from tkinter import ttk
import sqlite3
import webbrowser
from random import randrange
#make database
conn = sqlite3.connect("scholarship.db")
cursor = conn.cursor()

#open window
window = Tk()
window.title("scholarbot")
window.configure(background="white")
window.geometry("700x600")
resultindex = 1

matched = []

class Person:
    def __init__(self, heritage, school, fos, ros, gender,pc): 
        self.heritage = []
        self.school = []
        self.fos = []
        self.ros = []
        self.pc = []
        self.gender = []

#define user
user = Person([],[],[],[],[],[])

#for links
def callback(url):
    webbrowser.open_new_tab(url)

def title_page():
    #declare vars`
    global frame_title
    global title
    global btn_start
    #frame
    frame_title = Frame(window,pady=50,background="white")
    #title label
    title = Label(frame_title,fg="#1874CD",
            text="ScholarSwipe",
            bg="white",
            font=('BOLD', 40),
            height= 5,
            width = 10)
    #btn label
    btn_start = Button(frame_title, 
            text = "Start",
            command=start )
    #pack item
    frame_title.pack()
    title.grid(row=0,column=0)
    btn_start.grid(row=2,column=0)

def save():

    #save fos
    user.fos.clear()
    user.fos.append(fos.get()) 
    print(user.fos[0])

    #save school
    user.school.clear()
    user.school.append(school.get())
    print(user.school[0])

    #save ros
    user.ros.clear()
    user.ros.append(ros.get())
    print(user.ros[0])
    
    #save heritage
    user.heritage.clear()
    user.heritage.append(heritage.get())
    print(user.heritage[0])

    #save pc
    user.pc.clear()
    user.pc.append(pc.get())
    print(user.pc[0])

    #save gender
    user.gender.clear()
    user.gender.append(gender.get())
    print(user.gender[0])
        
    #clear screen    
    frame_query.destroy()
    
    #load swipe
    
    swipe()
   
def swipe():
    swipeframe = Frame(window,pady=10,padx=10, background="white")
    swipeframe.place(in_=window, anchor="c", relx=.5, rely=.5)
    
    #get number of scholarships
    
    count = cursor.execute("SELECT COUNT(*) FROM scholarships")
    rslt = count.fetchone()
    count = rslt[0]
    
    flag = True
    
    while flag:
    #choose random number for random scholarship
        ssid = randrange(count)
        print(ssid)
    #get random scholarship
        ss = cursor.execute("SELECT * FROM scholarships WHERE id=?",(ssid,))
        result = ss.fetchone()

        if result != None:
            flag = False

        

    ss1 = Frame(swipeframe, background="blue",highlightbackground="black",highlightthickness=2)
    ss1.grid(row=1,column=1,columnspan=2)
    
    url = result[4]

    viewmore = Button(swipeframe, font=("Futura",20),fg="#1874CD", background="white",borderwidth=0, text= "View More", command = lambda:callback(url))
    viewmore.grid(row=3,column=1, columnspan=2, pady=5)

    name = Label(ss1, text=result[1],height=4,width=22,wraplength=300,fg="white", borderwidth=2, font="standard-block 20", background="blue").grid(row=0, column=1, sticky='ew')
    amt = Label(ss1, text=result[2],font="standard-block 20", height=4, background="green").grid(row=1, column=1, sticky='ew')
    date = Label(ss1, text=result[3],height=4,font="standard-block 20", background="yellow").grid(row=2, column=1, sticky='ew')
    

    right = Button(swipeframe,command= lambda: yah(swipeframe,ssid),fg="#1874CD", text=">>",height=5,width=4, font=("Arial", 45),background="white",borderwidth=0)
    right.grid(row=1,column=4)

    
    left = Button(swipeframe, text="<<",command= lambda: nah(swipeframe),height=5,fg = "#1874CD",width=4, font=("Arial", 45),background="white",borderwidth=0)
    left.grid(row=1,column=0)
    
    saved = Button(swipeframe,borderwidth=0, text="matches",command= lambda: matches(swipeframe), background="white")
    saved.grid(row=0,column=4,pady=5)

    conn.commit()

def matches(frame):
    frame.destroy()
    matchview = Frame(window, background="white",padx=1)
    matchview.place(in_=window)

    Label(matchview,text="Scholarship Name", bg="white").grid(row=0,column=0, sticky="W")
    
    Label(matchview,text="Cash Amount", bg="white").grid(row=0,column=1, sticky="W")
    
    Label(matchview,text="Deadline", bg="white").grid(row=0,column=2, sticky="W")

    Label(matchview,text="Apply", bg="white").grid(row=0,column=3, sticky="W")
    for index in range(len(matched)-1):
        #get info        
        ss = cursor.execute("SELECT * FROM scholarships WHERE id=?",(matched[index],))
        results = ss.fetchone()
        
        #make label
        Label(matchview,text=results[1]).grid(row=index+1, column=0,sticky="W",pady=2,padx=8) 
        Label(matchview,text=results[2]).grid(row=index+1, column=1,sticky="W",pady=2,padx=8)
        Label(matchview,text=results[3]).grid(row=index+1, column=2,sticky="W",pady=2,padx=8)
        link = Label(matchview,text="link",fg="blue", font=("Arial 12 underline"))
        link.grid(row=index+1, column=3,sticky="W",pady=2,padx=8)
        link.bind("<Button-1>", lambda e:callback(results[4]))

    back = Button(matchview,  text="Go Back", command= lambda: nah(matchview),font=("Arial 20"),bg ="white", bd=0)
    back.grid(row=len(matched)+1, column=0, pady="8",sticky="W")
def nah(frame):
    frame.destroy()
    swipe()

def yah(frame,ssid):
    matched.append(ssid)
    frame.destroy()
    swipe()
    print(matched) 
def indexchange(index):
    if str(index.widget) == ".!frame3":
        print("hip:")
        resultindex = 0
    elif str(index.widget) == ".!frame4":
        print("jo")
        resultindex = 1
#make comboboxes searchable
def search(event):
    value = event.widget.get()
    
    #check which input value came from so we know what result list to use
    results = resultslists[resultindex]
    
     
    if value == ' ':
        event.widget['values'] = results

    else:
        data = []

        for item in results:
            if value.lower() in item.lower():
                data.append(item)
        fos['values'] = data
#transitions program to query process
def start():
   frame_title.destroy()
   query()

#Get info from user
def query():
    #declare vars
    global frame_query 
    global fos, school, ros, heritage, pc, gender
    global resultslists
    global fosresults, schoolresults, rosresults, genderresults, pcresults, heritageresults
#optionmenu vars
    
    
    #table for dropdowns
    fosresults = []
    schoolresults = []
    rosresults = []
    heritageresults = []
    pcresults = []
    genderresults = []

    #make list of result lists
    resultslists = []
    resultslists.append(fosresults)
    resultslists.append(schoolresults)
    resultslists.append(rosresults)
    resultslists.append(heritageresults)
    resultslists.append(pcresults)
    resultslists.append(genderresults)

    #query for fos names and populate fos list
    fosquery = cursor.execute("SELECT name FROM FOS")
    fosquery = fosquery.fetchall()
    
    for item in fosquery:
        fosresults.append(str(item[0]))

    #query for school names and populate school list
    schoolquery = cursor.execute("SELECT name FROM schools")
    schoolquery = schoolquery.fetchall()

    for item in schoolquery:
        schoolresults.append(str(item[0]))
    
    #query for heritage names and populate heritage list
    heritagequery = cursor.execute("SELECT name FROM heritage")
    heritagequery = heritagequery.fetchall()

    for item in heritagequery:
        heritageresults.append(str(item[0]))

    #query for ros names and populate ros list
    rosquery = cursor.execute("SELECT name FROM ROS")
    rosquery = rosquery.fetchall()
    
    for item in rosquery:
        rosresults.append(str(item[0]))

    #query for pc names and pc heritage list
    pcquery = cursor.execute("SELECT name FROM pc")
    pcquery = pcquery.fetchall()
    
    for item in pcquery:
        pcresults.append(str(item[0]))

    #populate gender list
    genderresults.extend(["male", "female", "rather not say"])
#frame
    frame_query = Frame(window,background="white", highlightbackground= "black",highlightthickness=2)
    frame_query.place(in_=window, anchor="c", relx=.5, rely=.5)
#query questions
    
    #fos dropdown | resultindex = 0
    fosframe = Frame(frame_query,pady=30,padx=20, background="white")
    fosframe.pack()
    fosframe.bind('<Enter>',indexchange)
    foslabel = Label(fosframe, text="What field of study are you taking?", background="white").pack()
    fos = ttk.Combobox(fosframe, value=fosresults,width="70")
    fos.current(0)
    fos.pack()
       
    #search function
    fos.bind('<KeyRelease>',search)
   
    #school dropdown | resultindex = 0
    schoolframe = Frame(frame_query,pady=5,padx=20, background="white")
    schoolframe.pack()
    schoolframe.bind('<Enter>',indexchange)
    schoollabel = Label(schoolframe, text="what school do you plan on attending?", background="white").pack()
    school = ttk.Combobox(schoolframe, value=schoolresults,width="70")
    school.current(0)
    school.pack()
    
    #ros dropdown | resultindex = 2
    rosframe = Frame(frame_query, pady=5,padx=20, background="white")
    rosframe.pack()
    rosframe.bind('<Enter>', indexchange)
    roslabel = Label(rosframe, text="what region are you planning on studying in?", background="white").pack()
    ros = ttk.Combobox(rosframe, value=rosresults, width="70")
    ros.current(0)
    ros.pack()
    
    #heritage dropdown | resultindex = 3
    heritageframe = Frame(frame_query, pady=5,padx=20, bg ="white")
    heritageframe.pack()
    heritageframe.bind('<Enter>', indexchange)
    heritagelabel = Label(heritageframe, text="what is your heritage?", background="white").pack()
    heritage = ttk.Combobox(heritageframe, value=heritageresults, width="70")
    heritage.current(0)
    heritage.pack()

    #personal circumstance | resultindex = 4
    pcframe = Frame(frame_query, pady=5,padx=20,bg="white")
    pcframe.pack()
    pcframe.bind('<Enter>', indexchange)
    pclabel = Label(pcframe, text="Do you have any personal circumstance?", background="white").pack()
    pc = ttk.Combobox(pcframe, value=pcresults, width="70")
    pc.current(0)
    pc.pack()

    #gender | resultindex = 5
    genderframe = Frame(frame_query, pady=5,padx=20, bg="white")
    genderframe.pack()
    genderframe.bind('<Enter>', indexchange)
    genderlabel = Label(genderframe, text="Choose your Gender?", background="white").pack()
    gender = ttk.Combobox(genderframe, value=genderresults, width="70")
    gender.current(0)
    gender.pack()

    #next button (saves data and clears page)
    button = Button(frame_query, text="Next",command=save).pack(pady=8)
    

title_page()
window.mainloop()
