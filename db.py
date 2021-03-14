import sqlite3
from os import path

def createDB():
    db = sqlite3.connect("timetable.db")
    my_cursor = db.cursor()
    my_cursor.execute(
        "CREATE TABLE timetable (name TEXT, start_time TEXT, end_time TEXT, day TEXT)")
    db.commit()
    db.close()
    print("Created database")


def add_timetable():
    if(not(path.exists("timetable.db"))):
        createDB()
    op = int(input("1. Add meeting\n2. Exit\nEnter option : "))
    while(op == 1):
        name = input("Enter meeting name: ")
        start_time = input(
            "Enter meeting start time (24 hour format) (HH:MM): ")

        end_time = input("Enter meeting end time (24 hour format): (HH:MM) ")

        day = input("Enter day : ")

        db = sqlite3.connect('timetable.db')
        mycursor = db.cursor()

        mycursor.execute("INSERT INTO timetable VALUES ('%s','%s','%s','%s')" % (
            name, start_time, end_time, day))

        db.commit()
        db.close()

        print("Meeting added to database\n")

        op = int(input("1. Add meeting\n2. Exit\nEnter option : "))


def view_timetable():
    db = sqlite3.connect('timetable.db')
    mycursor = db.cursor()
    for row in mycursor.execute('SELECT * FROM timetable'):
        print(row)
    db.close()
