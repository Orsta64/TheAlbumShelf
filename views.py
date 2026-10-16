from errno import EUSERS

from flask import Flask, render_template, request, Blueprint, redirect, url_for, session, flash
from jinja2.compiler import generate
from werkzeug.security import generate_password_hash, check_password_hash

from db import db_connection

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html', username=session['username'])

@views.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = db_connection()
        username = connection.execute(
            "SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        connection.close()

        if username and check_password_hash(username["password_hash"], password):
            session['username'] = username["username"]
            flash("Successfully Logged in", category="success")
            return redirect(url_for("views.profile"))

        flash("Password Incorrect", category="incorrect")

        return redirect(url_for("views.profile"))
    else:
        if "username" in session:
            return redirect(url_for("views.profile"))
        return render_template("login.html")





@views.route("<username>")
def user(username):
    return render_template('index.html', username=username)

@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        connection = db_connection()
        existing = connection.execute(
            "SELECT 1 FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            flash("Email Already Exists", category="error")
            connection.close()

        connection.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash)
        )
        connection.commit()
        connection.close()

        flash("Account Successfully Created", category="success")

        connection = db_connection()
        existing = connection.execute(
            "SELECT 1 FROM users WHERE email = ?", (email,)
        ).fetchone()



        session.permanent=True
        session['username'] = username
        return redirect(url_for('views.login',))
    else:
        return render_template('register.html')



@views.route("/profile")
def profile():
    if "username" in session:
        return redirect(url_for('views.user', username=session['username']))
    else:
        return render_template('login.html')

@views.route('/records')
def records():
    return render_template('records.html')

@views.route('/account', methods=['GET', 'POST'])
def account():
    if "username" not in session:
        return redirect(url_for('views.login'))

    if request.method == 'POST':
        new_username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        connection = db_connection()

        if password:
            password_hash = generate_password_hash(password)

            connection.execute(
                """
                UPDATE users
                SET username = ?, email = ?, password_hash = ?
                WHERE username = ?
                """,
                (new_username, email, password_hash, session['username'])
            )
        else:
            connection.execute(
                """
                UPDATE users
                SET username = ?, email = ?
                WHERE username = ?
                """,
                (new_username, email, session['username'])
            )

        connection.commit()
        connection.close()

        # Update the session because the username may have changed
        session['username'] = new_username

        return redirect(url_for('views.account'))

    return render_template(
        'account.html',
        username=session['username']
    )


@views.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('views.login'))

@views.route('/dsotm')
def dsotm():
    return render_template('albums/dsotm.html')

@views.route('/queen')
def queen():
    return render_template('albums/queen.html')

@views.route('/RHCP')
def RHCP():
    return render_template('albums/redhotchillipeppers.html')

@views.route('/LZT')
def LZT():
    return render_template('albums/ledzep.html')

@views.route('/PAN')
def PAN():
    return render_template('albums/paranoid.html')

@views.route('/ARM')
def ARM():
    return render_template('albums/am.html')

@views.route('/BB')
def BB():
    return render_template('albums/bb.html')

@views.route('/NRB')
def NRB():
    return render_template('albums/nvb.html')