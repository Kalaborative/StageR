# import the necessary modules
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from time import sleep
from os import environ

# start a Flask app
app = Flask(__name__)

# Declare global variables
firstUserData = []

# The makedata function handles new user registration on any page.
def makedata():
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		# pull name data from history table
		c.execute("SELECT name FROM history")
		histdata = c.fetchall()
		# this code flattens the list
		histdata = [h[0] for h in histdata]
		inputsex = request.form["sex"]
		inputname = request.form["discordtag"]
		# declare a match var that will tell if the for loop finds a match or not
		match = False
		# the default batch
		batch = [(inputsex, inputname, 0)]
		for hist in histdata:
			if inputname == hist:
				c.execute("SELECT singTimes FROM history WHERE name=?", [(inputname)])
				actualTimes = c.fetchone()[0]
				match = True
				batch = [(inputsex, inputname, actualTimes)]
		c.executemany("INSERT INTO current VALUES(?,?,?)", batch)
		if not match:
			c.executemany("INSERT INTO history VALUES(?,?,?)", batch)

# the default route decorator
@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		makedata()
		return redirect(url_for("index"))
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		c.execute("SELECT * FROM current")
		myUsers = c.fetchall()
		global firstUserData
		# if the length of users is more than 0, we need to pull the first name
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return render_template("index.html", users=myUsers, first=firstUserData)

# decorator for the 'next' button
@app.route('/next', methods=["GET", "POST"])
def nextSinger():
	if request.method == "POST":
		makedata()
		with sqlite3.connect("tags.db") as connection:
			c = connection.cursor()
			c.execute("SELECT * FROM current")
			myUsers = c.fetchall()
			global firstUserData
			if len(myUsers) > 0:
				firstUserData = myUsers.pop(-0)
			else:
				firstUserData = None
			return render_template("index.html", users=myUsers, first=firstUserData)
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		# when next is clicked, we need to increment the times he/she has sang by 1.
		# as well as remove the user from the 'current' queue.
		singer = (firstUserData[1])
		c.execute("UPDATE history SET singTimes = singTimes + 1 WHERE name=?", [singer])
		c.execute("DELETE FROM current WHERE name=?", [singer])
		c.execute("SELECT * FROM current")
		myUsers = c.fetchall()
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return render_template("index.html", users=myUsers, first=firstUserData)

# decorator for the 'skip' button
@app.route('/skip', methods=["GET", "POST"])
def skipSinger():
	if request.method == "POST":
		makedata()
		with sqlite3.connect("tags.db") as connection:
			c = connection.cursor()
			c.execute("SELECT * FROM current")
			myUsers = c.fetchall()
			global firstUserData
			if len(myUsers) > 0:
				firstUserData = myUsers.pop(-0)
			else:
				firstUserData = None
			return render_template("index.html", users=myUsers, first=firstUserData)
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		singer = (firstUserData[1])
		# here, we don't need to increment. Just delete the record in current.
		c.execute("DELETE FROM current WHERE name=?", [singer])
		c.execute("SELECT * FROM current")
		myUsers = c.fetchall()
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return render_template("index.html", users=myUsers, first=firstUserData)

# decorator for resetting the history data
@app.route('/resetd', methods=["GET", "POST"])
def resetHistory():
	if request.method == "POST":
		makedata()
		with sqlite3.connect("tags.db") as connection:
			c = connection.cursor()
			c.execute("SELECT * FROM current")
			myUsers = c.fetchall()
			global firstUserData
			if len(myUsers) > 0:
				firstUserData = myUsers.pop(-0)
			else:
				firstUserData = None
			return render_template("index.html", users=myUsers, first=firstUserData)
	with sqlite3.connect('tags.db') as connection:
		c = connection.cursor()
		c.execute("DELETE FROM history")
		sleep(2)
		c.execute("SELECT * FROM current")
		myUsers = c.fetchall()
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return render_template("index.html", users=myUsers, first=firstUserData)


if __name__ == "__main__":
	# convention to run on Heroku
	port = int(environ.get("PORT", 5000))
	# run the app available anywhere on the network, on debug mode
	app.run(host='0.0.0.0', port=port, debug=True)
