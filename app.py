from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		with sqlite3.connect("tags.db") as connection:
			c = connection.cursor()
			inputsex = request.form["sex"]
			inputname = request.form["discordtag"]
			batch = [(inputsex, inputname, 0)]
			c.executemany("INSERT INTO userdata VALUES(?,?,?)", batch)
			return redirect(url_for("index"))
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
		c.execute("SELECT * FROM userdata")
		myUsers = c.fetchall()
	return render_template("index.html", users=myUsers)

@app.route('/next')
def nextSinger():
	with sqlite3.connect("tags.db") as connection:
		c = connection.cursor()
if __name__ == "__main__":
	app.run(debug=True)