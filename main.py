import pickle
import math
from random import randint
from authentication import get_user
from noun_extract import extract_nouns

# users = {}
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
				print "replacing index with item", ret, (item[0], item[1])
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

if __name__ == '__main__':	
	username = get_user(2022, 219)
	print
	print "Hello", username
	print
	users = pickle.load(open('pickled/user_auth.p', 'rb'))
	cloud = users[username][3]
	print "Cloud is currently", cloud
	max_cloud = 20
	index = 0
	while(True):	

		# new users presented with random movie until they have voted and generated a cloud
		if cloud == []: 
			print "To get started, we suggest the following:"
			index = get_movie()
		else:
			print "Select focus items from cloud"
			focus_inputs = raw_input()
			focus_line = []
			for item in focus_inputs.split(','): focus_line.append(item)
			print focus_line

			# the focus_line is a list of words either clicked from cloud or otherwise 
			index = get_fitting_movie(focus_line) 
			print "Based on your decisions, we suggest the following:"
			index = get_movie(index)
			
		rating = request_rating(index)
		
		# a positive rating updates the user's movies, big list, and cloud	
		if int(rating) == 1:
			update_user_movies(index, 1)
			update_user_big_array(index)
			cloud = update_user_cloud(cloud, max_cloud)
			print cloud

		# a negative rating updates the user's movies, but not the big list or cloud
		elif int(rating) == -1:
			update_user_movies(index, -1)
			print cloud

		# a rating of zero is equivalent to pass
		elif int(rating) == 0:
			print cloud
			pass
