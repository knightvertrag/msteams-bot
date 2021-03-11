import sqlite3
from os import path
import re


def validate_input(regex, inp):
    if not re.match(regex, inp):
        return False
    return True


def validate_day(inp):
    days = ["monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday"]

    if inp.lower() in days:
        return True
    else:
        return False


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
    op = int(input("1. Add class\n2. Exit\nEnter option : "))
    while(op == 1):
        name = input("Enter class name: ")
        start_time = input(
            "Enter class start time (24 hour format) (HH:MM): ")
        while not(validate_input("\d\d:\d\d", start_time)):
            print("Invalid input, try again")
            start_time = input(
                "Enter class start time (24 hour format): (HH:MM) ")

        end_time = input("Enter class end time (24 hour format): (HH:MM) ")
        while not(validate_input("\d\d:\d\d", end_time)):
            print("Invalid input, try again")
            end_time = input(
                "Enter class end time (24 hour format): (HH:MM) ")

        day = input("Enter day : ")
        while not(validate_day(day.strip())):
            print("Invalid input, try again")
            end_time = input("Enter day : ")

        db = sqlite3.connect('timetable.db')
        mycursor = db.cursor()

        mycursor.execute("INSERT INTO timetable VALUES ('%s','%s','%s','%s')" % (
            name, start_time, end_time, day))

        db.commit()
        db.close()

        print("Class added to database\n")

        op = int(input("1. Add class\n2. Exit\nEnter option : "))

def view_timetable():
    db = sqlite3.connect('timetable.db')
    mycursor = db.cursor()
    for row in mycursor.execute('SELECT * FROM timetable'):
        print(row)
    db.close()
