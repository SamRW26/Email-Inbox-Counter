import re
import sqlite3

email_from = None

conn = sqlite3.connect('emaildbSW.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (email_from TEXT, email_address TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'test.txt'
fh = open(fname, encoding='utf8')
for line in fh:
    if not line.startswith('From: '):
        continue
    line_of_mail_address = line.split()

    for x in line_of_mail_address:
        if re.search('\"(.*)\"', x):
            email_from_temp = str(re.findall('\"(.*)\"', x))
            email_from = email_from_temp[2:-2]
            print(email_from)

    for address in line_of_mail_address:
        if re.search('@', address):
            email_address_temp = str(re.findall('<(.*)>', address))
            email_address = email_address_temp[2:-2]

    cur.execute('SELECT count FROM Counts WHERE email_from = ? ', (email_from,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (email_from, email_address, count)
                VALUES (?, ?, 1)''', (email_from, email_address, ))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE email_from = ?',
                    (email_from,))
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT email_from, email_address, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print('Email Details:', str(row[0]), row[1], row[2])
    if count % 500 == 0 : conn.commit()
    if count % 1000 == 0 : time.sleep(1)

conn.commit()
cur.close()
