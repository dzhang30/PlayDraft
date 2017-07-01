from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.sqlite3'
db = SQLAlchemy(app)

from api import api_module as _api
app.register_blueprint(_api)


if __name__ == '__main__':
    app.run(debug=True)
