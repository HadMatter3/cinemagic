import pickle
import math
import os
from random import randint
from authentication import get_user
from noun_extract import extract_nouns
import sys
from PyQt4 import QtGui, QtCore

big_array_size = 2022
movie_array_size = 219
max_cloud = 20

index = 0
username = ""
cloud = []
users = {}
# pickle.dump(users, open('pickled/user_auth.p', 'wb'))

# print users[username]

movies = pickle.load(open('pickled/pickled_movies.p', 'rb'))
# print movies

movie_words = pickle.load(open('pickled/pickled_movie_words.p', 'rb'))
# print movie_words

directed_by = pickle.load(open('pickled/pickled_directed_by.p', 'rb'))
# print directed_by

movie_genres = pickle.load(open('pickled/pickled_movie_genres.p', 'rb'))
# print movie_genres

movie_stars = pickle.load(open('pickled/pickled_starring.p','rb'))
# print movie_stars

descriptions = pickle.load(open('pickled/pickled_descriptions.p', 'rb'))
# print description

big_list = pickle.load(open('pickled/big_list.p', 'rb'))
# print big_list


def get_movie(index = None):
	if index == None: index = randint(0,219)
	print "Title...........", movies[index]
	print "Directed by.....", directed_by[index]
	for item in movie_stars[index] : print "Starring........", item
	for item in movie_genres[index] : print "Genre...........", item
	print "Synnopsis.......", descriptions[index]
	return index

def request_rating(index):
	print "Rate this movie:"
	rating = raw_input()
	return rating

def update_user_movies(index, rating):
	users[username][2][index] = int(rating)
	
def update_user_cloud(cloud, cloud_max):
	cloud = []
	for item in zip(users[username][1], big_list):
		if (item[0] != 0):
			if (len(cloud) < cloud_max): cloud.append((item[0],item[1]))
			else:
				min_weight = cloud[0][0]
				i = 0
				ret = 0
				for cloud_item in cloud: 
					if cloud_item[0] < min_weight:
						min_weight = cloud_item[0] 
						ret = i
					i += 1
				# print "replacing index with item", ret, (item[0], item[1])
				cloud[ret] = (item[0], item[1])
	return cloud

def update_user_big_array(index):
	i = 0
	for item in big_list:
		if item in movie_words[index]:
			# print "Hit for item", item 
			users[username][1][i] += 1
		i += 1
	# print "Cuture soup is", users[username][1]

def get_fitting_movie(focus_line):
	global users
	# perform cosin similarity, taking weights into consideration
	top_movie_score = 0
	top_movie_index = 0
	i = 0
	for movie in users[username][2]:
		if movie == 0:
			# print "checking movie...", movies[i]
			A_dot_B = 0
			D1 = 0
			D2 = math.sqrt(len(movie_words[i]))
			for item in zip(users[username][1], big_list):
				D1 += item[0]**2
				weight = 1
				if item[0] != 0:
					if item[1] in movie_words[i]:
						if item[1] in focus_line and focus_line != []: weight = 100
						A_dot_B += weight * item[0]

			D1 = math.sqrt(D1)
			# print "Rated", A_dot_B/(D1*D2)
			if A_dot_B/(D1*D2) > top_movie_score: 
				top_movie_score = A_dot_B/(D1*D2)
				top_movie_index = i

		i += 1
	#print movie_words[top_movie_index]
	return top_movie_index

class MovieWidget(QtGui.QWidget):
	def __init__(self):
		super(MovieWidget, self).__init__()
		self.initLoginUI()

	def login(self):
		global username
		if str(self.usertext.text()) not in users:
			self.statuslabel.setText("User not valid")
		elif str(self.pwdtext.text()) == users[str(self.usertext.text())][0]:
			self.label.hide()
			self.loginlabel.hide()
			self.usertext.hide()
			self.pwdtext.hide()
			self.createlabel.hide()
			self.newusertext.hide()
			self.newpwdtext.hide()
			self.newpwdtext2.hide()
			self.existingloginbutton.hide()
			self.newloginbutton.hide()
			self.statuslabel.hide()
			self.clearbutton.hide()
			
			username = str(self.usertext.text())
			
			self.initRatingsUI()
		else:
			self.statuslabel.setText("Password not valid")

	def create(self):
		global username
		if str(self.newusertext.text()) in users:
			self.statuslabel.setText("User already exists")
		elif str(self.newpwdtext.text()) != str(self.newpwdtext2.text()):
			self.statuslabel.setText("Passwords do not match")
		else:
			self.label.hide()
			self.loginlabel.hide()
			self.usertext.hide()
			self.pwdtext.hide()
			self.createlabel.hide()
			self.newusertext.hide()
			self.newpwdtext.hide()
			self.newpwdtext2.hide()
			self.existingloginbutton.hide()
			self.newloginbutton.hide()
			self.statuslabel.hide()
			self.clearbutton.hide()

			users[str(self.newusertext.text())] = [str(self.newpwdtext.text()), [0]*big_array_size, [0]*movie_array_size, []]
			pickle.dump(users, open('pickled/user_auth.p', 'wb'))
			username = str(self.newusertext.text())
			
			self.initRatingsUI()

	def initLoginUI(self):
		self.setGeometry(200, 200, 500, 500)
		self.setWindowTitle('Cinemagic')
		# creates window		

		self.label = QtGui.QLabel("", self)
		self.label.setGeometry(QtCore.QRect(50, -50, 400, 400))
		myPixmap = QtGui.QPixmap("film_reel.png")
		scaledPixmap = myPixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
		self.label.setPixmap(scaledPixmap)
		# intro image

		self.loginlabel = QtGui.QLabel("Login", self)
		self.loginlabel.setGeometry(QtCore.QRect(75, 350, 100, 25))
		# login

		self.usertext = QtGui.QLineEdit(self)
		self.usertext.move(75, 375)
		self.usertext.setPlaceholderText("Username")
		# username field

		self.pwdtext = QtGui.QLineEdit(self)
		self.pwdtext.move(75, 400)
		self.pwdtext.setPlaceholderText("Password")
		# password field

		self.createlabel = QtGui.QLabel("New User", self)
		self.createlabel.setGeometry(QtCore.QRect(250, 350, 100, 25))
		# new user

		self.newusertext = QtGui.QLineEdit(self)
		self.newusertext.move(250, 375)
		self.newusertext.setPlaceholderText("Username")
		# new user field

		self.newpwdtext = QtGui.QLineEdit(self)
		self.newpwdtext.move(250, 400)
		self.newpwdtext.setPlaceholderText("Password")
		# new password field

		self.newpwdtext2 = QtGui.QLineEdit(self)
		self.newpwdtext2.move(250, 425)
		self.newpwdtext2.setPlaceholderText("Confirm Password")
		# confirm new password field

		self.existingloginbutton = QtGui.QPushButton("Login", self)
		self.existingloginbutton.clicked.connect(self.login)
		self.existingloginbutton.move(75, 425)
		# login an old user
		
		self.newloginbutton = QtGui.QPushButton("Create", self)
		self.newloginbutton.clicked.connect(self.create)
		self.newloginbutton.move(250, 450)
		# create a new user
		
		self.clearbutton = QtGui.QPushButton("Clear Users", self)
		self.clearbutton.clicked.connect(self.clear)
		self.clearbutton.move(75, 450)
		
		self.statuslabel = QtGui.QLabel("", self)
		self.statuslabel.setGeometry(QtCore.QRect(75, 325, 200, 25))
		# login status

		self.titlelabel = QtGui.QLabel("", self)
		self.posterlabel = QtGui.QLabel("", self)
		self.genrelabel = QtGui.QLabel("", self)
		self.starslabel = QtGui.QLabel("", self)
		self.directorlabel = QtGui.QLabel("", self)
		self.descriptionlabel = QtGui.QLabel("", self)
		self.cloudlabel = QtGui.QLabel("", self)
		self.upvotebutton = QtGui.QPushButton(QtGui.QIcon(QtGui.QPixmap("upvote.png")), "", self)
		self.upvotebutton.clicked.connect(self.upvote)
		downmap = QtGui.QPixmap("downvote.png")		
		self.downvotebutton = QtGui.QPushButton(QtGui.QIcon(QtGui.QPixmap("downvote.png")), "", self)
		self.downvotebutton.clicked.connect(self.downvote)
		self.upvotebutton.hide()
		self.downvotebutton.hide()
		# Used on Ratings UI
		
		self.show()

	def displayMovie(self):
		self.titlelabel.setGeometry(QtCore.QRect(0, 0, 500, 25))
		self.titlelabel.setText(movies[index])
		self.titlelabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
		font = self.titlelabel.font()
		font.setPixelSize(self.titlelabel.height()*.8)
		self.titlelabel.setFont(font)
		# title of movie
		
		self.posterlabel.setGeometry(QtCore.QRect(10, 35, 200, 250))
		pixmap = QtGui.QPixmap("pics/%s.jpg" % movies[index])
		scaledpixmap = pixmap.scaled(self.posterlabel.size(), QtCore.Qt.KeepAspectRatio)
		self.posterlabel.setPixmap(scaledpixmap)
		# poster of movie
		
		genrestring = "Genre: "
		for g in movie_genres[index]:
			genrestring += g
			if g != movie_genres[index][-1]:
				genrestring += "/"
		self.genrelabel.setGeometry(QtCore.QRect(200, 50, 290, 25))
		self.genrelabel.setText(genrestring)
		self.genrelabel.setWordWrap(True)
		# genre of movie
		
		self.directorlabel.setGeometry(QtCore.QRect(200, 75, 290, 25))
		self.directorlabel.setText("Director: %s" % directed_by[index])
		self.directorlabel.setWordWrap(True)
		# director of movie
		
		starringstring = "Starring: "
		for s in movie_stars[index]:
			if s == movie_stars[index][-1]:
				starringstring += "and "
			starringstring += s
			if s != movie_stars[index][-1]:
				starringstring += ", "
		self.starslabel.setGeometry(QtCore.QRect(200, 90, 290, 50))
		self.starslabel.setText(starringstring)
		self.starslabel.setWordWrap(True)
		# stars of movie
		
		self.descriptionlabel.setGeometry(QtCore.QRect(200, 120, 290, 100))
		self.descriptionlabel.setText(descriptions[index])
		self.descriptionlabel.setWordWrap(True)
		# synopsis of movie
		
		self.upvotebutton.move(420, 400)
		self.downvotebutton.move(420, 450)
		self.upvotebutton.show()
		self.downvotebutton.show()
		# vote buttons
	
	def upvote(self):
		global cloud, index, users
		update_user_movies(index, 1)
		update_user_big_array(index)
		cloud = update_user_cloud(cloud, max_cloud)
		users[username][3] = cloud
		pickle.dump(users, open('pickled/user_auth.p', 'wb'))
		self.printCloud()

		if cloud == []:
			print "To get started, we suggest the following:"
			index = get_movie()
		else:
#			print "Select focus items from cloud"
#			focus_inputs = raw_input()		
			focus_line = []
#			for item in focus_inputs.split(','): focus_line.append(item)
#			print focus_line		
			
			index = get_fitting_movie(focus_line)
			print "Based on your cloud, we suggest the following:"
			index = get_movie(index)
		
		self.displayMovie()
		# gets new movie
	# positive rating

	def downvote(self):
		global index
		update_user_movies(index, -1)
		if cloud != []:
			self.printCloud()

		if cloud == []:
			print "To get started, we suggest the following:"
			index = get_movie()
		else:
#			print "Select focus items from cloud"
#			focus_inputs = raw_input()		
			focus_line = []
#			for item in focus_inputs.split(','): focus_line.append(item)
#			print focus_line		
			
			index = get_fitting_movie(focus_line)
			print "Based on your cloud, we suggest the following:"
			index = get_movie(index)
		
		self.displayMovie()
	# negative rating
	
	def printCloud(self):
		self.cloudlabel.setGeometry(100, 300, 300, 200)
		self.cloudlabel.setText("%s" % str(cloud))
		self.cloudlabel.setWordWrap(True)		
	
	def initRatingsUI(self):
		global username, cloud, index
		cloud = users[username][3]
		
		self.setWindowTitle("Recommendations for %s" % username)
		
		# new users presented with random movie until they have voted and generated a cloud
		if cloud == []:
			print "To get started, we suggest the following:"
			index = get_movie()
		else:
			self.printCloud()
#			print "Select focus items from cloud"
#			focus_inputs = raw_input()
			focus_line = []
#			for item in focus_inputs.split(','): focus_line.append(item)
#			print focus_line

			# the focus_line is a list of words either clicked from cloud or otherwise 
			index = get_fitting_movie(focus_line) 
			print "Based on your decisions, we suggest the following:"
			index = get_movie(index)
		
		self.displayMovie()
	
	def clear(self):
		users = {}
		pickle.dump(users, open('pickled/user_auth.p', 'wb'))
		
if __name__ == '__main__':
	users = pickle.load(open('pickled/user_auth.p', 'rb'))
	app = QtGui.QApplication(sys.argv)
	window = MovieWidget()
	sys.exit(app.exec_())
