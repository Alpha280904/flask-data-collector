from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)  # Creates the Flask web app


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    color = db.Column(db.String(50))

with app.app_context():
    db.create_all()
user_data = []

@app.route('/', methods=['GET', 'POST'])  # The homepage
def home():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        color = request.form['color']
        user_data.append({'name': name, 'age': age, 'color': color})

        conn = sqlite3.connect('instance/database.db')
        c = conn.cursor()
        c.execute("INSERT INTO user (name, age, color) VALUES (?,?,?)", (name, age, color))
        conn.commit()
        conn.close()

        # return redirect('/users')
        return redirect(url_for('thank_you', username=name))
    return render_template('home.html')


@app.route('/thankyou/<username>')
def thank_you(username):
    return f"<h2>Thanks, {username}! Your data has been saved.</h2><a href='/'>Submit Another</a></p>"

@app.route('/users')
def users():
    conn = sqlite3.connect('instance/database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user")
    users = c.fetchall()
    conn.close()
    return render_template('users.html', users=users)
if __name__ == '__main__':
    app.run(debug=True)
