#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('picture_share.db')

c = conn.cursor()

# Turn on foreign key support
c.execute("PRAGMA foreign_keys = ON")

# Create users table
c.execute('''CREATE TABLE users
	     (email TEXT NOT NULL, 
	      password TEXT NOT NULL,
	      firstName TEXT,
	      lastName TEXT,
	      picture TEXT,
	      FOREIGN KEY (picture) REFERENCES pictures(path),
	      PRIMARY KEY(email))''')

# Create album table
# Visibility is 'public' or 'private'
c.execute('''CREATE TABLE albums
	     (name TEXT NOT NULL,
	      owner TEXT NOT NULL,
	      visibility TEXT NOT NULL,
	      FOREIGN KEY (owner) REFERENCES users(email),
	      PRIMARY KEY(name, owner))''')

# Create pictures table
c.execute('''CREATE TABLE pictures
	     (path TEXT NOT NULL,
	      album TEXT NOT NULL,
	      owner TEXT NOT NULL,
	      FOREIGN KEY(album, owner) REFERENCES albums(name, owner),
	      FOREIGN KEY(owner) REFERENCES users(email),
	      PRIMARY KEY(path))''')

# Create sessions table
c.execute('''CREATE TABLE sessions
	     (user TEXT NOT NULL,
	      session TEXT NOT NULL,
	      FOREIGN KEY(user) REFERENCES users(email),
	      PRIMARY KEY(session))''')

c.execute('''CREATE TABLE circles
	     (user TEXT NOT NULL,
	      name TEXT NOT NULL,
	      FOREIGN KEY(user) REFERENCES users(email),
	      PRIMARY KEY(user, name))''')

# Creates a user friend table
c.execute('''CREATE TABLE friendlist
	     (user TEXT NOT NULL,
	      circle TEXT NOT NULL,
	      friend TEXT NOT NULL,
	      FOREIGN KEY(user) REFERENCES users(email),
	      FOREIGN KEY(circle) REFERENCES circles(name),
	      FOREIGN KEY(friend) REFERENCES users(email),
	      PRIMARY KEY(user))''')

# Save the changes
conn.commit()

# Close the connection
conn.close()
