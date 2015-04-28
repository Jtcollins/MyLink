#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('picture_share.db')
c = conn.cursor()

print
print 'Print all users'
for row in c.execute('SELECT * FROM users'):
  print row

print
print "Print peter's password"
t = ('peter@gmail.com',)
c.execute('SELECT * FROM users WHERE email=?', t)
print c.fetchone()[1]


print 'Print all posts'
for row in c.execute('SELECT * FROM posts'):
  print row


print 'Print all friendslist'
for row in c.execute('SELECT * FROM friendlist'):
  print row

print 'Print all circles'
for row in c.execute('SELECT * FROM circles'):
  print row