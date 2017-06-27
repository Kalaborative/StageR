import sqlite3
with sqlite3.connect("tags.db") as connection:
	c = connection.cursor()
	c.execute("DROP TABLE IF EXISTS userdata")
	c.execute("CREATE TABLE userdata (sex TEXT, name TEXT)")
