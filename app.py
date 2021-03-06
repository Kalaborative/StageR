# import the necessary modules
from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
import sqlite3
from random import choice
from time import sleep
from os import environ, urandom
from functools import wraps

# start a Flask app
app = Flask(__name__)
app.secret_key = urandom(24)


# Declare global variables
firstUserData = []
animals = ["beach.png","mouse.png","dolphine.png","crab.png","bee.png","rabbit.png","tiger.png","owl.png","elephant.png","panda.png","snail.png","frog.png","fish.png","reindeer.png","lion.png","bear.png","spider.png","butterfly.png","spider2.png","animals1.png","animals2.png","animals3.png","animals4.png","animal6.png","animal7.png",]


# The makedata function handles new user registration on any page.
def makedata():
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		# pull name data from history table
		c.execute("SELECT name FROM history")
		histdata = c.fetchall()
		# this code flattens the list
		histdata = [h[0] for h in histdata]
		inputan = choice(animals)
		inputname = request.form["discordtag"]
		# declare a match var that will tell if the for loop finds a match or not
		match = False
		# the default batch
		batch = [(inputan, inputname, 0, 0, 0)]
		for hist in histdata:
			if inputname == hist:
				c.execute("SELECT * FROM history WHERE name=?", [(inputname)])
				actualTimes = c.fetchone()
				match = True
				batch = [actualTimes]
		c.executemany("INSERT INTO current VALUES(?,?,?,?,?)", batch)
		if not match:
			c.executemany("INSERT INTO history VALUES(?,?,?,?,?)", batch)
			c.executemany("INSERT INTO permanent VALUES(?,?,?,?,?)", batch)


# login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		try:
			if not session['logged_in']:
				return render_template('error.html')
		except KeyError:
			return render_template('error.html')
		return f(*args, **kwargs)
	return wrap

# the default route decorator
@app.route("/")
def index():
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		c.execute("SELECT * FROM current")
		myUsers = c.fetchall()
		# if the length of users is more than 0, we need to pull the first name
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return render_template("public.html", users=myUsers, first=firstUserData)

@app.route("/refresh", methods=['POST'])
def refresh():
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		c.execute("SELECT * FROM current")
		myUsers = c.fetchall()
		# if the length of users is more than 0, we need to pull the first name
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return jsonify({"firstUserData": firstUserData, "myUsers": myUsers})


@app.route('/av', methods=["GET", "POST"])
@login_required
def adminview():
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
		# if the length of users is more than 0, we need to pull the first name
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return render_template("index.html", users=myUsers, first=firstUserData)

@app.route("/adminlogin", methods=["GET", "POST"])
def login():
	error = None
	if request.method == "POST":
		if request.form["username"] == "org123" and request.form["password"] == "#L0v3sh4ck":
			session['logged_in'] = True
			return redirect(url_for('adminview'))
		else:
			error = True
			return render_template('login.html', error=error)
	return render_template("login.html", error=error)

# decorator for the 'next' button
@app.route('/av/next', methods=["GET", "POST"])
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
		userLikes = (firstUserData[3])
		userDisLikes = (firstUserData[4])
		singer = (firstUserData[1])
		c.execute("UPDATE history SET singTimes = singTimes + 1 WHERE name=?", [singer])
		c.execute("UPDATE permanent SET singTimes = singTimes + 1 WHERE name=?", [singer])
		c.execute("UPDATE history SET likes = ? WHERE name=?", [userLikes, singer])
		c.execute("UPDATE history SET dislikes = ? WHERE name=?", [userDisLikes, singer])
		c.execute("UPDATE permanent SET dislikes = ? WHERE name=?", [userDisLikes, singer])
		c.execute("UPDATE permanent SET likes = ? WHERE name=?", [userLikes, singer])
		c.execute("DELETE FROM current WHERE name=?", [singer])
		c.execute("SELECT * FROM current")
		myUsers = c.fetchall()
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return redirect(url_for("adminview"))

# decorator for the 'skip' button
@app.route('/av/skip', methods=["GET", "POST"])
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
		return redirect(url_for('adminview'))

# decorator for resetting the history data
@app.route('/resetd', methods=["GET", "POST"])
@login_required
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
		return redirect(url_for('adminview'))


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
	editType = "del"
	if request.method == "POST":
		deleteUser = (request.form['slct'])
		with sqlite3.connect('tags.db') as connection:
			c = connection.cursor()
			c.execute("DELETE FROM current WHERE name=?", [deleteUser])
			return redirect(url_for('adminview'))
	with sqlite3.connect('tags.db') as connection:
		c = connection.cursor()
		c.execute("SELECT name FROM current")
		allNames = c.fetchall()[1:]
		allNames = [a[0] for a in allNames]
		return render_template("edit.html", edit=editType, names=allNames)

@app.route("/rename", methods=["GET", "POST"])
@login_required
def rename():
	editType = "ren"
	if request.method == "POST":
		oldUser = request.form['slct']
		newUser = request.form['newname']
		changeUser = (newUser, oldUser)
		with sqlite3.connect('tags.db') as connection:
			c = connection.cursor()
			c.execute("UPDATE current SET name=? WHERE name=?", changeUser)
			c.execute("DELETE FROM history WHERE name=?", [oldUser])
			c.execute("DELETE FROM permanent WHERE name=?", [oldUser])
			c.execute("SELECT name FROM history")
			match = False
			histNames = c.fetchall()
			for h in histNames:
				if newUser == h:
					match = True
			if not match:
				c.execute("INSERT INTO history VALUES(?,?,?,?,?)", (choice(animals), newUser, 0, 0, 0))
				c.execute("INSERT INTO permanent VALUES(?,?,?,?,?)", (choice(animals), newUser, 0, 0, 0))
			return redirect(url_for('adminview'))
	with sqlite3.connect('tags.db') as connection:
		c = connection.cursor()
		c.execute("SELECT name FROM current")
		allNames = c.fetchall()[1:]
		allNames = [a[0] for a in allNames]
	return render_template("edit.html", edit=editType, names=allNames)

@app.route('/log')
def log():
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		c.execute("SELECT * FROM current")
		myUsers = c.fetchall()
		if len(myUsers) > 0:
			firstUserData = myUsers.pop(-0)
		else:
			firstUserData = None
		return render_template('log.html', users=myUsers, first=firstUserData)

@app.route('/logfull')
def fullLog():
	return render_template('fulllog.html')

@app.route('/stats')
@login_required
def stats():
	with sqlite3.connect('tags.db') as connection:
		c = connection.cursor()
		c.execute("SELECT singTimes from permanent")
		allTimes = c.fetchall()
		realTimes = [a[0] for a in allTimes]
		totalTimes = sum(realTimes)
		percentages = []
		for r in realTimes:
			pctvalue = int(round((r * 1.00 / totalTimes) * 100))
			percentages.append(pctvalue)
		c.execute("SELECT name from permanent")
		allNames = c.fetchall()
		realNames = [a[0] for a in allNames]
		statData = zip(realNames, percentages)
		c.execute("SELECT name, likes from permanent")
		allLikes = c.fetchall()
		allLikes = sorted(allLikes, key=lambda d: d[1], reverse=True)
		try:
			mostLiked = allLikes[0][0]
		except:
			mostLiked = ""
		c.execute("SELECT name, dislikes from permanent")
		allDislikes = c.fetchall()
		allDislikes = sorted(allDislikes, key=lambda d: d[1], reverse=True)
		try:
			mostDisliked = allDislikes[0][0]
		except:
			mostDisliked = ""
		return render_template('stats.html', stats=statData, msliked=mostLiked, msdsliked=mostDisliked)

@app.route("/l", methods=["POST"])
def votelike():
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		c.execute("SELECT * from current")
		currentNameData = c.fetchone()
		nameDataName = currentNameData[1]
		c.execute("UPDATE current SET likes = likes + 1 WHERE name=?", [nameDataName])
		c.execute("SELECT * from current")
		currentNameData = c.fetchone()
		return jsonify({"status": "OK", "likes": currentNameData[3]})

@app.route("/dl", methods=["POST"])
def votedislike():
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		c.execute("SELECT * from current")
		currentNameData = c.fetchone()
		nameDataName = currentNameData[1]
		c.execute("UPDATE current SET dislikes = dislikes + 1 WHERE name=?", [nameDataName])
		c.execute("SELECT * FROM current")
		currentNameData = c.fetchone()
		return jsonify({"status": "OK", "dislikes": currentNameData[4]})	


@app.route('/featured')
def featured():
	return render_template('feature.html')


if __name__ == "__main__":
	# convention to run on Heroku
	port = int(environ.get("PORT", 5000))
	# run the app available anywhere on the network, on debug mode
	app.run(host="0.0.0.0", port=port, debug=True)
