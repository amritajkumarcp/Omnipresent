import sqlite3
import os, json

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "app/static/", "init_data.json")
users = json.load(open(json_url))

for user in users:
    cur.execute("INSERT INTO users (firstName, lastName, dateOfBirth, jobTitle, company, country) VALUES (?, ?, ?, ?, ?, ?)",
            (list(user.values()))
            )

connection.commit()
connection.close()