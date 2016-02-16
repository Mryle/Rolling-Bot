import sqlite3 as lite

base = lite.connect('resources/gng.sqlite')
cur = base.cursor()

def getNames(table, cond):
   cur.execute("SELECT name FROM " + table + " WHERE " + cond)
   rows = cur.fetchall()
   rtext = ''
   for row in rows:
      rtext = rtext + str(row) + '\n'
   return rtext

def getRecord(table, name):
   cur.execute("SELECT * FROM " + table + " WHERE name='" + name + "'")
   rows = cur.fetchone()
   rtext = ''
   for row in rows:
      rtext = rtext + str(row) + '\n'
   return rtext

#Aliases

def getAllNames(table):
   return getNames(table,"name LIKE '%'")

def getNotes():
   return getAllNames('notes')

def getNote(name):
   return getRecord('notes',name)

def addNote(name,desc):
   cur.execute("INSERT INTO notes (name,desc) \
      VALUES ('" + name + "','" + desc + "')")
   base.commit()

def deleteNote(name):
   cur.execute("DELETE FROM notes WHERE name=" + name)
   base.commit()
