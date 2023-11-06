from flask import session, Flask, request, redirect, render_template, url_for

app = Flask(__name__)
# Set the session key to some random bytes. Keep this secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
	if 'username' in session:
		return f'Logged in as {session["username"]}'
	return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for('index'))
	return '''
		<form method="post">
			<p><input type="text" name="username"></p>
			<p><input type="submit" value="Login"></p>
		</form>
	'''

@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	return redirect(url_for('index'))

app.run(debug=True)