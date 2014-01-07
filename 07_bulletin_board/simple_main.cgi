#!/usr/bin/python

print 'Content-type: text/html\n'

import cgitb; cgitb.enable()

import psycopg2
import psycopg2.extras
conn = psycopg2.connect('dbname=test user=postgres password=postgres host=localhost')

curs = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)


print """
<html>
  <head>
    <title>The FooBar Bulletin Board</title>
  </head>
  <body>
    <h1>The FooBar Bulletin Board</h1>
"""

curs.execute('SELECT * FROM messages')
rows = curs.fetchall()

toplevel = []
children = {}

for row in rows:
    parent_id = row['reply_to']
    if parent_id is None:
        toplevel.append(row)
    else:
        children.setdefault(parent_id,[]).append(row)


def format(row):
    print row['subject']
    try:
        kids = children[row['id']]
    except KeyError:
        pass
    else:
        print '<blockquote>'
        for kid in kids:
            format(kid)
        print '</blockquote>'

print '<p>'
for row in toplevel:
    format(row)

print """
</p>
</body>
</html>
"""
