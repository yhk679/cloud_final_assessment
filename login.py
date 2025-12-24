#!/usr/bin/env python3

import cgi
import pymysql

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
username = form.getvalue("username")
password = form.getvalue("password")

# RDS Connection
conn = pymysql.connect(
    host="YOUR_RDS_ENDPOINT",
    user="YOUR_DB_USER",
    password="YOUR_DB_PASSWORD",
    database="cms"
)

cursor = conn.cursor()

query = "SELECT * FROM users WHERE username=%s AND password=%s"
cursor.execute(query, (username, password))

result = cursor.fetchone()

if result:
    print("""
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=/index.html">
    </head>
    <body>
        Login successful. Redirecting...
    </body>
    </html>
    """)
else:
    print("""
    <html>
    <body>
        <h3>Login Failed</h3>
        <a href="/login.html">Try again</a>
    </body>
    </html>
    """)

cursor.close()
conn.close()
