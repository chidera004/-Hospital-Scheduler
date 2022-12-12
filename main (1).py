# Importing our SQL library and other inputs
import sqlite3  # library used for the database control
import os  # to have access to our os
import datetime  # to authenticate date and time
import re

# ======================================================== Creating our database ===============================================
if os.path.exists('Database.db'):
    conn = sqlite3.connect('Database.db')  # Connecting to the database (Database.db)
    cur = conn.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS signup(username VARCHAR(30), email VARCHAR(30) UNIQUE, password VARCHAR(50))''')
    # cur.execute('''DROP TABLE IF EXISTS appointment''')
    cur.execute('''CREATE TABLE IF NOT EXISTS appointment (name VARCHAR(50), reasonForAppointment VARCHAR(50), user_inputted_time DATETIME UNIQUE)''')
    conn.commit()

else:
    conn = sqlite3.connect('Database.db')
    cur = conn.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS signup(username VARCHAR(30), email VARCHAR(30) UNIQUE, password VARCHAR(50))''')
    # cur.execute('''DROP TABLE IF EXISTS appointment''')
    cur.execute('''CREATE TABLE IF NOT EXISTS appointment (name VARCHAR(50), reasonForAppointment VARCHAR(50),user_inputted_time DATETIME)''')
    conn.commit()

name = ''
rfa = ''
# =========================================================== Login function ==================================================


def login():
    print('enter your details \n')
    username = input('Enter username: ')  # Username input
    email = input('Enter email: ')  # email input
    password = input('Enter password: ')  # Password input

    cur.execute('SELECT * FROM signup WHERE username=? and email=? and password=?',
                [username, email, password])  # Searching through our database for the inputs
    # If login details are  in database then login
    if cur.fetchone() is None:  # if there are no match for the inputs then retry the login
        print('Login Details Error... Try again')
        login()
    else:
        print('Login successful')
        appointment()  # redirect to our appointment function if the login is successfully


# =============================================================== Signup function ==============================================
def signup():
    print('\n all sections are required\n')
    while True:
        username = input('Username: ')  # Username
        if len(username) == 0:
            print("This field must not be empty")
            continue
        elif username.isnumeric():
            print("numbers aren't allowed")
            continue
        elif username.__contains__(' '):
            print("Space are not allowed...")
            continue
        elif len(username) != 0:
            break

    pattern = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'
    while True:
        email = input('Enter email: ')  # email
        if re.search(pattern, email):
            print('valid email address')
            break

        elif len(email) == 0:
            print("This field must not be empty")
            continue
        else:
            print('invalid email address')
            continue
    cur.execute('''SELECT * FROM signup WHERE email=?''', [email])
    if cur.fetchone():
        print('Email already exists...Signup Again')
        conn.commit()
        return main()
    while True:
        while True:
            password = input('password: ')  # password
            if len(password) < 8:
                print("Password must not be less than 8")
                continue
            elif len(password) >= 8:
                break

        c_password = input('confirm your password: ')
        if password != c_password:
            print('password mismatch')
            continue
        elif password == c_password:
            print("Password Matches")
            break

    try:
        sql = '''INSERT INTO signup(username, email, password) VALUES(?, ?, ?)'''
        var = (username, email, password)
        # Saving our input info into our database
        cur.execute(sql, var)
        conn.commit()
        print('Signup successful!!\n Login: ')
        # Redirecting back to our login function
        login()
    except sqlite3.IntegrityError:
        print("Email already exists")


# ==================================================Appointment function=======================================================
def appointment():
    global name
    global rfa
    print('Would you like to book an appointment Yes/No  (NO: Auto-logged out !!!): ')
    a = input()  # input function to confirm appointments
    if a.lower() == 'yes':
        nameApp = input('Name : ')  # Name input
        name = nameApp
        while True:
            reasonForAppointment = input('Reason for appointment: ')  # reason for appointment input
            rfa = reasonForAppointment
            if rfa.isascii():
                break
            else:
                print("Only letters are allowed")
                continue
        getDate()
    elif a.lower() == 'no':
        print('Have a great day ')
        main()
    else:
        print("Wrong input")
        appointment()
    # If appointment details are  in database then confirm appointment


def getDate():
    while True:
        while True:
            day = input("Enter the day dd: ")
            if day.isdigit():
                if len(day) == 2:
                    break
                elif len(day) != 2:
                    print("2 characters(numbers) were expected")
                    continue
            elif not day.isdigit():
                print("Only numbers are allowed")
                continue
        while True:
            month = input("Enter the month mm: ")
            if month.isdigit():
                if len(month) == 2:
                    break
                elif len(month) != 2:
                    print("2 characters(numbers) were expected")
                    continue
            elif not month.isdigit():
                print("Only numbers are allowed")
                continue
        while True:
            year = input("Enter the year yyyy: ")
            if year.isdigit():
                if len(year) == 4:
                    break
                elif len(year) != 4:
                    print("4 characters(numbers) were expected")
                    continue
            elif not year.isdigit():
                print("Only numbers are allowed")
                continue
        print("You have chosen " + day + '-' + month + '-' + year)
        while True:
            print("Enter the time in 24hrs format")
            hours = input("Enter the hour hh: ")
            if hours.isdigit():
                if len(hours) == 2:
                    break
                elif len(hours) != 2:
                    print("2 characters(numbers) were expected")
                    continue
            elif not hours.isdigit():
                print("Only numbers are allowed")
        while True:
            minutes = input("Enter the minute MM: ")
            if minutes.isdigit():
                if len(minutes) == 2:
                    break
                elif len(minutes) != 2:
                    print("2 characters(numbers) were expected")
                    continue
            elif not minutes.isdigit():
                print("Only numbers are allowed")

        currentDate = datetime.datetime.today()
        dd = int(day)
        mm = int(month)
        yyyy = int(year)
        hh = int(hours)
        mint = int(minutes)

        if mm == 1 or mm == 3 or mm == 5 or mm == 7 or mm == 8 or mm == 10 or mm == 12:
            max_days = 31
        elif mm == 4 or mm == 6 or mm == 9 or mm == 11:
            max_days = 30
        elif yyyy % 4 == 0 and yyyy % 100 != 0 or yyyy % 400 == 0:
            max_days = 29
        else:
            max_days = 28

        if mm < 1 or mm > 12:
            print("Invalid Date... Check the range of month")
            continue
        elif dd < 1 or dd > max_days:
            print("Invalid Date... Check the range of day")
            continue
        elif hh < 9 or hh > 17:
            print("Wrong  Timing... DOCTOR IS UNAVAILABLE")
            continue
        elif mint < 0 or mint > 59:
            print("Invalid Time... Check the range of minutes")
            continue
        elif mm < 1 or mm > 12 and dd < 1 or dd > max_days:
            print("Invalid Date... Check the range of month and day")
            continue
        elif mm < 1 or mm > 12 and hh < 1 or hh > 24:
            print("Invalid Date and Time... Check the range of month and hour")
        elif mm < 1 or mm > 12 and mint < 0 or mint > 59:
            print("Invalid Date and Time... Check the range of month and minute")
        elif dd < 1 or dd > max_days and hh < 0 or hh > 23:
            print("Invalid Date and Time... Check the range of day and hour")
        else:
            authDate(day, month, year, hours, minutes, currentDate)
            break


def authDate(day, month, year, hours, minutes, currentDate):
    while True:
        formatted_date = day + '-' + month + '-' + year + ' ' + hours + ':' + minutes
        user_inputted_date = datetime.datetime.strptime(formatted_date, "%d-%m-%Y %H:%M")
        if user_inputted_date < currentDate:
            print("The data passed is the past....pls input correct date ")
            getDate()
            continue
        elif user_inputted_date >= currentDate:
            print("Date confirmed")
            print(user_inputted_date)
            cur.execute('''SELECT * FROM appointment WHERE user_inputted_time=?''', [user_inputted_date])
            if cur.fetchone() is None:
                # Inserting variable values into our Database
                code = '''INSERT INTO appointment(name, reasonForAppointment, user_inputted_time) VALUES(?, ?, ?)'''
                variable = (name, rfa, user_inputted_date)
                cur.execute(code, variable)
                conn.commit()
                print('Appointment successful')
                appointment()
            else:
                print('appointment date taken')
                return appointment()
            break


# =================================================== Main function ========================================================
def main():
    print('Welcome to PYTHON HOSPITAL  . '
          '\nPress 1 to login '
          '\n Press 2 to Signup'
          '\nPress 3 to end the program ')
    while True:
        ans = input()
        if ans == '1':
            login()
            break
        elif ans == '2':
            signup()
            break
        elif ans == '3':
            break
        else:
            print('You have to enter 1, 2 or 3 ')
            continue


if __name__ == '__main__':
    main()
