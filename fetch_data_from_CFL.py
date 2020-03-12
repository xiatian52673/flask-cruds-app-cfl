from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from App_player import Player
from App_game import Game
import requests

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "cfl.db"))

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

url1 = 'http://api.cfl.ca/v1/players'
PARAMS1 = {'page[number]': 1, 'page[size]': 100, 'key': 'T8Mv9BRDdcB7bMQUsQvHqtCGPewH5y8p'}
num_inserted_ids = 0
inserted_ids = set()
while num_inserted_ids < 100:
    res1 = requests.get(url1, params=PARAMS1)
    json_obj1 = res1.json()
    for player in json_obj1['data']:
        if player['cfl_central_id'] in inserted_ids:
            continue
        new_player = Player(player['cfl_central_id'], player['stats_inc_id'], player['first_name'],
                            player['middle_name'], player['last_name'], player['birth_date'], player['birth_place'],
                            player['height'], player['weight'], player['rookie_year'], player['foreign_player'],
                            player['school']['school_id'], player['school']['name'],
                            player['position']['position_id'], player['position']['offence_defence_or_special'],
                            player['position']['abbreviation'], player['position']['description'])
        db.session.add(new_player)
        inserted_ids.add(player['cfl_central_id'])
        num_inserted_ids += 1
        if num_inserted_ids >= 100:
            break

    PARAMS1['page[number]'] += 1
db.session.commit()
print(num_inserted_ids, " players are inserted")




url2 = 'http://api.cfl.ca/v1/games/2018'
PARAMS2 = {'key': 'T8Mv9BRDdcB7bMQUsQvHqtCGPewH5y8p'}
num_inserted_games = 0
inserted_games = set()
res2 = requests.get(url2, params=PARAMS2)
json_obj2 = res2.json()
for game in json_obj2['data']:
    if game['game_id'] in inserted_games:
        continue
    game['date_start'] = game['date_start'][:10]
    print(game['game_id'], game['date_start'], game['game_number'], game['week'], game['season'],
                    game['attendance'], game['game_duration'], game['event_type']['event_type_id'],
                    game['event_status']['event_status_id'], game['venue']['venue_id'],
                    game['team_1']['team_id'], game['team_2']['team_id'])
    new_game = Game(game['game_id'], game['date_start'], game['game_number'], game['week'], game['season'],
                    game['attendance'], game['game_duration'], game['event_type']['event_type_id'],
                    game['event_status']['event_status_id'], game['venue']['venue_id'],
                    game['team_1']['team_id'], game['team_2']['team_id'])
    db.session.add(new_game)
    inserted_games.add(game['game_id'])
    num_inserted_games += 1

db.session.commit()
print(len(inserted_games), " games are inserted")
