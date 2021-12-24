# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTextEdit
import sqlite3


session = {'username':'','password':'', 'userid': 0}

def selection():
    conn = sqlite3.connect('users.db')
    con = sqlite3.connect('notes.db')
    cur = conn.cursor()
    curr = con.cursor()
    print('users\n')
    cur.execute("""select * from users""")
    rows = cur.fetchall()
    for item in rows:
        print(item)
    
    print('end users\n')
    print('notes\n')
    curr.execute("""select * from notes""")
    rows = curr.fetchall()
    for item in rows:
        print(item)
    print('end notes\n')

def notedeletion(name, userid):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    delete_query = 'DELETE FROM notes WHERE name = ? and userid = ?'
    c.execute(delete_query, (name,userid))
    conn.commit()
    conn.close()


def notespreload(userid):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    select_query = "select name from notes where userid = ?"
    
    c.execute(select_query, (userid,))
    rows = c.fetchall()
    return rows

def descriptionselect(name):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    select_query = 'select description from notes where name = ?'
    
    c.execute(select_query, (name,))
    rows = c.fetchall()
    return rows[0][0]

def wipingdbusers():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS users""")
    
    conn.commit()
    conn.close()

def wipingdbnotes():
    conn = sqlite3.connect("notes.db")
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS notes""")
    
    conn.commit()
    conn.close()

def dbinitusers():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    userid INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT);
                                                        """)
    conn.commit()
    conn.close()

def dbinitnotes():
    
    conn = sqlite3.connect("notes.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS notes(
                    noteid INTEGER PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    userid INTEGER,
                    CONSTRAINT fk_notes
                    FOREIGN KEY (userid)
                    REFERENCES users(userid));
                                                        """)
    conn.commit()
    conn.close()


def registering(username,password):
    
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    user = (username,password)
    c.execute("INSERT INTO users (username, password) VALUES (?,?)",user)
    select_query = "select * from users"
    c.execute(select_query)
    print(c.fetchall())
    
    conn.commit()
    conn.close()	

def loginning(login,password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    select_query = "select * from users where username = ? and password = ?"

    c.execute(select_query, (login, password))
    rows = c.fetchall()
    
    
    if len(rows) == 0:
        logged_in = 0
       
    elif len(rows) == 1:
        logged_in = 1
        session['userid'] = int(rows[0][0])
    
    return logged_in
    

def addingnote(name,description,userid):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    note = (name,description,userid)
    c.execute("INSERT INTO notes (name, description, userid) VALUES (?,?,?)",note)
    select_query = "select * from notes"
    c.execute(select_query)
    print(c.fetchall())
    
    conn.commit()
    conn.close()

class start(QDialog):

    def __init__(self):
        super(start,self).__init__()
        loadUi("main screen.ui",self)
        self.tologin.clicked.connect(self.tologinfunc)
        self.toregister.clicked.connect(self.toregisterfunc)
        self.setWindowTitle('Start')
        self.setWindowIcon(QtGui.QIcon('pics/start.png'))

    def tologinfunc(self):
        self.cams = login()
        self.cams.show()
        self.close() 
    
    def toregisterfunc(self):
        self.cams = register()
        self.cams.show()
        self.close()

class login(QDialog):
    def __init__(self):
        super(login,self).__init__()
        loadUi("login.ui",self)
        self.tostart.clicked.connect(self.tostartfunc)
        self.toregister.clicked.connect(self.toregisterfunc)
        self.submit.clicked.connect(self.submitfunc)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.setWindowTitle('Login')
        self.setWindowIcon(QtGui.QIcon('pics/login.png')) 
        self.errormessage.setHidden(True)

    def submitfunc(self):
        username = self.username.text()
        password = self.password.text()
        # print(f'Logged in as: \nUsername: {username}\nPassword: {password}')
        
        result = loginning(username, password)
        
        if result == 1:
            session['username'] = username
            session['password'] = password
            self.tomainwindow()
        elif result == 0:
            self.errormessage.setHidden(False)
        else:
            self.errormessage.setHidden(False)
        
        
                
        
        

    def tostartfunc(self):
        self.cams = start()
        self.cams.show()
        self.close()
    
    def toregisterfunc(self):
        self.cams = register()
        self.cams.show()
        self.close()
    
    def tomainwindow(self): 
        self.cams = mainwindows()
        self.cams.show()
        self.close()
    
    

    
    

    
class register(QMainWindow):

    def __init__(self):
        super(register ,self).__init__()
        loadUi("register.ui",self)
        self.tostart.clicked.connect(self.tostartfunc)
        self.tologin.clicked.connect(self.tologinfunc)
        self.submit.clicked.connect(self.submitfunc)
        self.errormessage.setHidden(True)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.setWindowTitle('Register')
        self.setWindowIcon(QtGui.QIcon('pics/register.png'))

    def submitfunc(self):

        username = self.username.text()
        password = self.password.text()
        confirmpassword = self.confirmpassword.text()
        # print(f'Registered as: \nUsername: {username}\nPassword: {password}')
        if password == confirmpassword:
            
            try:
                registering(username,password)

            except sqlite3.Error as er:
                self.errormessage.setHidden(False)
            self.tologinfunc()
        else:
            self.errormessage.setHidden(False)
        

    def tostartfunc(self):
        self.cams = start()
        self.cams.show()
        self.close()
    
    def tologinfunc(self):
        self.cams = login()
        self.cams.show()
        self.close() 
    

class mainwindows(QMainWindow):
    def __init__(self):
        super(mainwindows,self).__init__()
        loadUi("mainwindow.ui",self)
        self.username.setText(session['username'])
        self.description.setHidden(True)
        self.name.setHidden(True)
        self.add.clicked.connect(self.addnote)
        self.finish.setHidden(True)
        self.finish.clicked.connect(self.submitnote)
        self.listWidget.clicked.connect(self.viewnote)
        self.wipe.clicked.connect(self.deletenote)
        self.logout.clicked.connect(self.logoutfunc)
        self.setWindowTitle('Notes')
        self.setWindowIcon(QtGui.QIcon('pics/notes.png'))
        notes = notespreload(session["userid"])
        for note in notes:
            self.listWidget.addItem(note[0])
        # print(notes)
        # for note in notes:
        #     print(note)
        #     self.listWidget.addItem(note)

    def viewnote(self):
        self.description.setHidden(False)
        self.name.setHidden(False)
        item = self.listWidget.currentItem().text()
        desc = descriptionselect(item)
        self.description.setText(desc)
        self.name.setText(item)

    def addnote(self):
        self.description.clear()
        self.name.clear()
        self.description.setHidden(False)
        self.name.setHidden(False)
        self.finish.setHidden(False)
        
    def submitnote(self):
        name = self.name.text()
        description = self.description.toPlainText()
        userid = session["userid"]
        addingnote(name,description,userid)
        self.listWidget.addItem(name)
        self.description.setHidden(True)
        self.name.setHidden(True)
        self.finish.setHidden(True)
        self.description.clear()
        self.name.clear()
    
    def deletenote(self):
        try:
            name = self.listWidget.currentItem().text()
            userid = session["userid"]
            index = self.listWidget.currentRow()
            notedeletion(name,userid)
            deleted = self.listWidget.takeItem(index)
        except Exception as ex:
            print(ex)
            
        print('deleted:',deleted)
        self.description.clear()
        self.name.clear()

    def logoutfunc(self):
        self.cams = start()
        self.cams.show()
        self.close()
        

        
# class noteedit(QMainWindow):
#     def __init__(self):
#         super(noteedit,self).__init__()
#         loadUi("edit.ui",self)


if __name__ == "__main__":
    selection()
    # wipingdbusers()
    # wipingdbnotes()
    dbinitusers()
    dbinitnotes()
    app = QApplication(sys.argv)
    mainwindow = start()
    mainwindow.show()
    try:
        sys.exit(app.exec_())
    except:
        print('exiting..')
    
