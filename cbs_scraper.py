import requests
from pprint import pprint
from main import db
from main import BasketBallPlayer, BaseBallPlayer, FootBallPlayer


URL = 'http://api.cbssports.com/fantasy/players/list?version=3.0&SPORT={}&response_format=JSON'
NFL_URL = 'http://api.cbssports.com/fantasy/players/list?version=3.0&SPORT=football&response_format=JSON'
MLB_URL = 'http://api.cbssports.com/fantasy/players/list?version=3.0&SPORT=baseball&response_format=JSON'


class CBS:
    def __init__(self):
        pass

    def get_players_by_sport(self, sport):
        """
        get all the players by sport in the required format
        :param sport: type of sport (basketball, baseball, or football)
        :return: list of players by sport in the required format
        """
        sport_type = sport.lower()
        r = requests.get(url=URL.format(sport.lower()))
        response_json = r.json()
        players = response_json['body']['players']

        avg_position_ages = self._compute_average_position_ages(players)
        for player in players:
            if 'age' in player and player['age'] is not None:  # players without an age are not active
                player['avg_position_age_diff'] = player['age'] - avg_position_ages[player['position']]
                self._store_player_in_db(sport_type, player)

    @staticmethod
    def _compute_average_position_ages(players):
        """
        get the average age for each position
        :param players: list of players
        :return: a map of each position to its average age
        """
        avg_position_ages = {}
        for player in players:
            if 'age' not in player or player['age'] is None:  # players without an age are not active
                continue
            if player['position'] not in avg_position_ages:
                avg_position_ages[player['position']] = [player['age'], 1]
            else:
                avg_position_ages[player['position']][0] += player['age']  # sum of ages by position
                avg_position_ages[player['position']][1] += 1  # number of players by position

        for position in avg_position_ages.keys():
            avg_position_ages[position] = avg_position_ages[position][0] / avg_position_ages[position][1]

        return avg_position_ages

    @staticmethod
    def _store_player_in_db(sport_type, player):
        """
        adds player into our database
        :param sport_type: type of sport
        :param player: specified player
        """
        if sport_type == 'basketball':
            player['name_brief'] = '{0} {1}.'.format(player['firstname'], player['lastname'][0])
        if sport_type == 'baseball':
            player['name_brief'] = '{0} {1}.'.format(player['firstname'][0], player['lastname'][0])
        if sport_type == 'football':
            player['name_brief'] = '{0} {1}.'.format(player['firstname'][0], player['lastname'])

        attributes = {
            'name_brief': player['name_brief'],
            'first_name': player['firstname'],
            'last_name': player['lastname'],
            'position': player['position'],
            'age': player['age'],
            'average_position_age_deff': player['avg_position_age_diff'],
            'id': player['id']
        }

        if sport_type == 'basketball':
            new_player_in_db = BasketBallPlayer(attributes)
        if sport_type == 'baseball':
            new_player_in_db = BaseBallPlayer(attributes)
        if sport_type == 'football':
            new_player_in_db = FootBallPlayer(attributes)

        db.session.add(new_player_in_db)
        db.session.commit()

    @staticmethod
    def _store_player_in_list(storage, sport, player):
        """
        store player into a list/array
        :param storage: list/array to store player info in
        :param sport: type of sport
        :param player: specified player
        """
        if sport == 'basketball':
            name_brief = '{0} {1}.'.format(player['firstname'], player['lastname'][0])
        if sport == 'baseball':
            name_brief = '{0} {1}.'.format(player['firstname'][0], player['lastname'][0])
        if sport == 'football':
            name_brief = '{0} {1}.'.format(player['firstname'][0], player['lastname'])

        storage.append(
            {
                'id': player['id'],
                'name_brief': name_brief,
                'first_name': player['firstname'],
                'last_name': player['lastname'],
                'position': player['position'],
                'age': player['age'],
                'average_position_age_diff': player['avg_position_age_diff']
            }
        )


if __name__ == '__main__':
    db.create_all()
    cbs = CBS()
    cbs.get_players_by_sport('baseball')
    cbs.get_players_by_sport('football')
    cbs.get_players_by_sport('basketball')
