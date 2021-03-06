'''
Tasks description:
==================

- Create a database table in RAM named 'Roster' that includes the fields
'Name', 'Species' and 'IQ'
- Populate you new table with the following values:
    Jean-Baptiste Zorg, Human, 122
    Korben Dallas, Meat Popsicle, 100
    Ak'not, Mangalore, -5

- Update the Species of Korben Dallas to be Human
- Display the names and IQs of everyone in the table who is classified
as Human.
'''

import sqlite3

defaultData = (
    ("Jean-Baptiste Zorg", "Human", 122),
    ("Korben Dallas", "Meat Popsicle", 100),
    ("Ak'not", "Mangalore", -5)
)

connection = sqlite3.connect(':memory:')
c = connection.cursor()
c.execute("DROP TABLE IF EXISTS Roster")
c.execute("CREATE TABLE Roster(Name TEXT, Species TEXT, IQ INT)")
c.executemany("INSERT INTO Roster VALUES(?, ?, ?)", defaultData)

# update species for Korben Dallas and print humans IQs
c.execute("UPDATE Roster SET Species=? WHERE Name=?",
         ('Human', 'Korben Dallas'))
c.execute("SELECT Name, IQ FROM Roster WHERE Species='Human'")
for row in c.fetchall():
    print row

connection.close()
