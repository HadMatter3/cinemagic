import pickle

def get_user(big_array_size, movie_array_size):
	# uers = {}
	# pickle.dump(users, open('pickled/user_auth.p', 'wb'))
	users = pickle.load(open('pickled/user_auth.p', 'rb'))

	print 'Username:',
	username = raw_input()
	if username not in users:
		print username, 'is not a valid user. Would you like to create a new user? (y/n)',
		confirm = raw_input()
		while True:
			if confirm == 'y':
				print 'Please enter a password for %s.' % username,
				pw = raw_input()
				print 'Please confirm password.',
				pw2 = raw_input()
				if pw != pw2:
					print 'Passwords must match.'
				else:
					# big_array_size = 2022
					# movie_array_size = 249
					# cloud_array_size = 15
					
					users[username] = [pw, [0]*big_array_size, [0]*movie_array_size, []]
					pickle.dump(users, open('pickled/user_auth.p', 'wb'))
					return username

			elif confirm == 'n':
				exit(0)
			else:
				print 'Must enter y or n:',
				confirm = raw_input()
	else:
		print 'Password:',
		password = raw_input()

		attempts = 1
		while attempts < 3:
			if password != users[username][0]:
				print 'Password incorrect.'
				print 'Password:',
				password = raw_input()
				attempts += 1
			else:
				return username
		if attempts >= 3:
			print 'Too many failed logins.'
			return 0

	print 'User', username, 'has successfully logged in.'
	return username