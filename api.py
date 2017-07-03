from flask import Blueprint, jsonify

api_module = Blueprint('api', __name__, url_prefix='/api')

from models import Player


@api_module.route('/players/all/<sport>')
def get_players_by_sport(sport):
    sport_type = get_type_from_sport(sport)
    if type is None:
        return "invalid url route"
    players = Player.query.filter_by(type=sport_type).all()
    return jsonify([player.to_json() for player in players])


@api_module.route('/players/<name_brief>')
def get_player_by_name(name_brief):
    player = Player.query.filter_by(name_brief=name_brief).first()
    return jsonify(player.to_json())


def get_type_from_sport(sport):
    sport_players = {
        'basketball': 'basketball player',
        'baseball': 'baseball player',
        'football': 'football player'
    }

    try:
        return sport_players[sport]
    except KeyError:
        return None
