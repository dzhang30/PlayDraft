from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.sqlite3'
db = SQLAlchemy(app)


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name_brief = db.Column(db.String(40))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    position = db.Column(db.String(10))
    age = db.Column(db.Integer)
    average_position_age_diff = db.Column(db.Float)
    type = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'player',
        'polymorphic_on': type
    }

    def __init__(self, kwargs):
        self.id = kwargs['id']
        self.name_brief = kwargs['name_brief']
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.position = kwargs['position']
        self.age = kwargs['age']
        self.average_position_age_diff = kwargs['average_position_age_deff']


class BasketBallPlayer(Player):
    __mapper_args__ = {
        'polymorphic_identity': 'basketball player'
    }


class BaseBallPlayer(Player):
    __mapper_args__ = {
        'polymorphic_identity': 'baseball player'
    }


class FootBallPlayer(Player):
    __mapper_args__ = {
        'polymorphic_identity': 'football player'
    }

# if __name__ == '__main__':
#     db.create_all()

