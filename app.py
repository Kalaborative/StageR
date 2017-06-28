from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from os import environ

app = Flask(__name__)

firstUserData = []

def makedata():
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		c.execute("SELECT name FROM history")
		histdata = c.fetchall()
		histdata = [h[0] for h in histdata]
		inputsex = request.form["sex"]
		inputname = request.form["discordtag"]
		match = False
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
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return render_template("index.html", users=myUsers, first=firstUserData)

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
		c.execute("DELETE FROM current WHERE name=?", [singer])
		c.execute("SELECT * FROM current")
		myUsers = c.fetchall()
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return render_template("index.html", users=myUsers, first=firstUserData)


@app.route('/start', methods=["GET", "POST"])
def startQueue():
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
		c.execute("SELECT * FROM current")
		myUsers = c.fetchall()
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return render_template("index.html", users=myUsers, first=firstUserData)

if __name__ == "__main__":
	port = int(environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=True)