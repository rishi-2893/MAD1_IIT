from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/target", methods=["POST"])
def target():
    userName = request.form['user_name']
    return render_template('target.html', user_name = userName)



if __name__ == '__main__':
    app.run(debug=True)