users = {}

file = open('user_auth.txt', 'r')
line = file.readline().strip()
while line != '':
	line = line.split(':')
	users[line[0]] = line[1]
	line = file.readline().strip()
file.close()

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
				file = open('user_auth.txt', 'a')
				file.write(username)
				file.write(":")
				file.write(pw)
				file.write("\n")
				break	
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
		if password != users[username]:
			print 'Password incorrect.'
			print 'Password:',
			password = raw_input()
			attempts += 1
		else:
			break
	if attempts >= 3:
		print 'Too many failed logins.'
		exit(0)

print 'User', username, 'has successfully logged in.'
