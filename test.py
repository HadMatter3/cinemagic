# use this file to check the pickling
# uncomment what you wish!

import pickle
from authentication import get_user

users = {}
pickle.dump(users, open('pickled/user_auth.p', 'wb'))

username = get_user(2022, 250)
# print "un is", username

users = pickle.load(open('pickled/user_auth.p', 'rb'))
print users[username]

# movies = pickle.load(open('pickled/pickled_movies.p', 'rb'))
# print movies

# directed_by = pickle.load(open('pickled/pickled_directed_by.p', 'rb'))
# print directed_by

# movie_genres = pickle.load(open('pickled/pickled_movie_genres.p', 'rb'))
# print movie_genres

# movie_stars = pickle.load(open('pickled/pickled_starring.p','rb'))
# print movie_stars

# users = pickle.load(open('pickled/user_auth.p', 'rb'))
# print users

# big_list = pickle.load(open('pickled/big_list.p', 'rb'))
# print big_list
