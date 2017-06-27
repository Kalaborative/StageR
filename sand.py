from bs4 import BeautifulSoup

with open("templates/index.html") as fp:
	soup = BeautifulSoup(fp)
	print soup