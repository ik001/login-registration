from tkinter import*
from tkinter.ttk import *
import sqlite3
import os
import io
from tkinter import messagebox as mb
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
import threading
import face_recognition as fr

win = Tk()

w = win.winfo_screenwidth()
h = win.winfo_screenheight()
win.geometry('{}x{}'.format(w,h))
#win.geometry('300x300')
var = 0
#LOGIN
x2 = StringVar()
y2 = StringVar()

#USER ID
l1 = Label(win,text = "USER ID")
l1.place(relx = 0.60,rely = 0.30)
en1 = Entry(win,width = 25,textvariable = x2)
en1.place(relx = 0.67,rely = 0.30)
#PASSWARD
l2 = Label(win,text = "PASSWARD")
l2.place(relx = 0.60,rely = 0.40)
en2 = Entry(win,width = 25,show = "*",textvariable = y2)
en2.place(relx = 0.67,rely = 0.40)
#LOGIN BUTTON
def login():
    db = sqlite3.connect("data.db")
    cr = db.cursor()
    ip = cr.execute("select EMPLOYEE,PASSWORD from reg WHERE EMPLOYEE = '"+x2.get()+"' AND PASSWORD = '"+y2.get()+"' ")
    for e in ip:
        print("Login succesfull")
        break
    else:
        mb.showinfo('Alert','Login Failed')
    db.commit()
    db.close()
    x2.set("")
    y2.set("")
b1 = Button(win,text = "LOGIN",command = login)
b1.place(relx = 0.73,rely = 0.45)
#FACE UNLOCK
tof = True
def faceunlock():
    #Dispplay video...
    global cap
    cap = cv.VideoCapture(0)
    l9 = Label(win)
    l9.place(relx =0.35,rely = 0.45)
    #DATABASE OUT
    arr = []
    global ee
    db = sqlite3.connect("data.db")
    cr = db.cursor()
    ic = cr.execute("select IMG,EMPLOYEE from reg")
    for e in ic:
        ee = e
        r = io.BytesIO(e[0])
        r = Image.open(r)
        r = np.array(r)      
        if fr.face_encodings(r):
                if len(r)>0:
                        arr.append(fr.face_encodings(r)[0])
                        break
                        
    db.commit()
    db.close()
    print(ee[1])
    def check(img):
        global tof
        imgi = fr.face_encodings(img)[0]
        print(len(arr ))
        if len(fr.face_encodings(img))>0:
                for e in arr:
                        if fr.compare_faces([e],imgi)[0] == True:#[True][0]
                            print("Welcome")
                            cap.release()
                            import fileA
                            win.destroy()
                            break
                        else:
                            print("You are not Registered")
        else:
                print("NPI")
    def show1():
        if(cap.isOpened()):
            
            _,img = cap.read()
            global tof
            if len(fr.face_encodings(img)) > 0:
                img = cv.cvtColor(img,cv.COLOR_RGB2BGR)
                check(img)
                return 1
            img = cv.resize(img,(200,200))
            img = Image.fromarray(img)
            
            img = ImageTk.PhotoImage(image = img)
            #img = img.resize((100,100))
            l9.img = img
            l9.configure(image = img)
            if tof == True:
                
                l9.after(5,show1)
   
    show1()    
   
    

b1 = Button(win,text = "FACE UNLOCK",command = faceunlock)
b1.place(relx = 0.67,rely = 0.60)

#REGESTER BUTTON
x1 = StringVar()
y1 = StringVar()
z1 = StringVar()
a1 = StringVar()

def reg():
    if var:
        cap.release()
    f1 = Toplevel()
    f1.geometry('500x400')
    #f1.place(x=0,y=0,width = 300,height = 300)
    l3 = Label(f1,text = "NAME")
    l3.place(relx = 0.10,rely = 0.10)
    en3 = Entry(f1,textvariable = x1)
    en3.place(relx = 0.50,rely = 0.10)
    l4 = Label(f1,text = "EMPLOYEE ID")
    l4.place(relx = 0.10,rely = 0.20)
    en4 = Entry(f1,textvariable = y1)
    en4.place(relx = 0.50,rely = 0.20)
    l5 = Label(f1,text = "CREATE PASSWORD")
    l5.place(relx = 0.10,rely = 0.30)
    en5 = Entry(f1,show = "*",textvariable = z1)
    en5.place(relx = 0.50,rely = 0.30)
    l6 = Label(f1,text = "CONFIRM PASSWORD")
    l6.place(relx = 0.10,rely = 0.40)
    en6 = Entry(f1,show = "*",textvariable = a1)
    en6.place(relx = 0.50,rely = 0.40)
    l7 = Label(f1,text = "SET UP FACE UNLOCK")
    l7.place(relx = 0.10,rely = 0.50)

    def addpicture():
        #Display video...
        
        cap = cv.VideoCapture(0)
        l8 = Label(f1)
        l8.place(relx =0.10,rely = 0.60)
        def show():
            
            _,img = cap.read()
            global ri
            ri = img#FOR STORAGE
            img = cv.cvtColor(img,cv.COLOR_RGB2BGR)
            img = cv.resize(img,(100,100))
            img = Image.fromarray(img)
            
            img = ImageTk.PhotoImage(image = img)
            #img = img.resize((100,100))
            l8.img = img
            l8.configure(image = img)
            l8.after(10,show)
        
        show()
        def closew():
            cap.release()
            f1.destroy()
        f1.protocol("WM_DELETE_WINDOW",closew)#ON CLOSING WINDOW
    b4= Button(f1,text = "ADD",command = addpicture)
    b4.place(relx = 0.50,rely = 0.50)
    def insert():
        if z1.get() == a1.get():
            
            if not os.path.exists('data.db'):
               db = sqlite3.connect('data.db')
               cr = db.cursor()
               cr.execute("create table reg(NAME text,EMPLOYEE text,PASSWORD text,IMG BLOB null)")
               db.commit()
               db.close()
            db = sqlite3.connect('data.db')
            cr = db.cursor()
            cr.execute("INSERT INTO reg(NAME,EMPLOYEE,PASSWORD,IMG)VALUES(?,?,?,?)",(x1.get(),y1.get(),z1.get(),bi))
            db.commit()
            db.close()
            
        else:
            mb.showinfo('Alert','Password Mismatch')
        x1.set("")
        y1.set("")
        z1.set("")
        a1.set("")
    b3 = Button(f1,text = "REGISTER",command = insert)
    b3.place(relx = 0.50,rely = 0.60)
    def setpic():
        global ri
        ri = cv.imencode('.jpg',ri)[1]
        ri = np.array(ri)
        ri = ri.tobytes()
        global bi
        bi = ri
    b5 = Button(f1,text = "SET",command = setpic)
    b5.place(relx = 0.35,rely = 0.80)
    
b2 = Button(win,text = "REGISTER",command = reg)
b2.place(relx = 0.90,rely = 0.09)

win.mainloop()
