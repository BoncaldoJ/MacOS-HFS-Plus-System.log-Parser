# Parsing system.log pre-APFS logfiles
# Justin Boncaldo 2018
# Adapted by Zachary Burnham 2019 (@zmbf0r3ns1cs)
# ----------------------------------------------------------

import re
import sqlite3

# Creates SQLite database
i = input("Enter full output filepath [FILE FORMAT: <name.db>]:")
connection = sqlite3.connect(i)
cursor = connection.cursor()
cursor.execute('CREATE TABLE System_logs (Month STRING, Date INTEGER, Time INTEGER, Process STRING, Message STRING)')

path = input("Enter target system.log filepath:")
f = open(path, encoding='utf-8')
blines = f.readlines()
f.close()

# Regex for files
Month = re.compile(r"\w{1,5}")
Date = re.compile(r"\d{1,2}")
Time = re.compile(r"\d{2}:\d{2}:\d{2}")
Process = re.compile(r'\w+\[.{1,5}]')
Message = re.compile(r': \w+.*$')

print("Parsing log file...")
for b in blines:
    matchTime = Time.search(b)
    matchDate = Date.search(b)
    matchMonth = Month.search(b)
    matchProcess = Process.search(b)
    matchMessage = Message.search(b)

    if (matchMonth and matchDate and matchTime and matchProcess and matchMessage):
        # Sets group values to new variables so only the match value is shown. Otherwise it shows match metadata
        a = matchMonth.group()
        b = matchDate.group()
        c = matchTime.group()
        d = matchProcess.group()
        e = matchMessage.group()

# Writes values to database file
        cursor.execute('INSERT INTO System_logs VALUES(?, ?, ?, ?, ?)', (str(a), str(b), str(c), str(d), str(e),))

# Creates database and saves.
        connection.commit()

print("Completed")
