import sqlite3
with sqlite3.connect("tags.db") as connection:
	c = connection.cursor()
	c.execute("DROP TABLE IF EXISTS current")
	c.execute("DROP TABLE IF EXISTS history")
	c.execute("DROP TABLE IF EXISTS userdata")
	c.execute("CREATE TABLE current (sex TEXT, name TEXT, singTimes INT)")
	c.execute("CREATE TABLE history (sex TEXT, name TEXT, singTimes INT)")