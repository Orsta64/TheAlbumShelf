from flask import Flask, render_template, session
from views import views
from datetime import timedelta
from db import init_db

app = Flask(__name__)


app.secret_key = "AKey"
app.permanent_session_lifetime = timedelta(days=5)
app.register_blueprint(views, url_prefix='/views')

init_db()

if __name__ == '__main__':
    app.run(debug=True, port=6200)