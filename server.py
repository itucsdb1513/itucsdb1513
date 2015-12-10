import datetime
import json
import os
import psycopg2 as dbapi2
import re

from turkah import Turkah
from events import event
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask.helpers import url_for
from player import Player
from rules import Rules
from ranking import Ranking
from history import facts
from player_info import Player_info

app = Flask(__name__)


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/rankings', methods=['GET', 'POST'])
@app.route('/rankings/<int:key>/', methods=['GET', 'POST'])
def rankings_page(key = None):
    page = Ranking(dsn = app.config['dsn'])
    if key == 1:
       return page.open_page("name")
    elif key == 2:
        return page.open_page("surname")
    elif key == 3:
        return page.open_page("country")
    elif key == 4:
        return page.open_page("club")
    elif key == 5:
        return page.open_page("age")
    elif key == 6:
        return page.open_page("rating")
    elif key == 7:
        return page.open_page("ranking")
    elif key == 8:
        return page.open_page("gender")
    elif request.method == 'GET':
        return page.open_page()
    elif 'initializeTable' in request.form:
        return page.init_table()
    elif 'addplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        country = request.form['country']
        club = request.form['club']
        rating = request.form['rating']
        ranking = request.form['ranking']
        age = request.form['age']
        gender = request.form['gender']
        return page.add_player(name, surname, country, club, rating, ranking, age, gender)
    elif 'deleteplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        return page.delete_player(name, surname)
    elif 'deleteplayerwithid' in request.form:
        id = request.form['id']
        return page.delete_player_with_id(id)
    elif 'findplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        return page.find_player(name, surname)
    elif 'findplayerbyrating' in request.form:
        rating = request.form['rating']
        return page.find_player_by_rating(rating)
    else:
        return redirect(url_for('home_page'))

@app.route('/update_ranking/<int:key>/', methods=['GET', 'POST'])
def update_ranking_page(key = None):
    page = Ranking(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.open_update_player(id = key)
    elif 'updateplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        country = request.form['country']
        club = request.form['club']
        rating = request.form['rating']
        ranking = request.form['ranking']
        age = request.form['age']
        gender = request.form['gender']
        return page.update_player(key, name, surname, country, club, rating, ranking, age, gender)
    else:
        return redirect(url_for('home_page'))

@app.route('/worldplayers_info', methods=['GET', 'POST'])
@app.route('/worldplayers_info/<int:key>/', methods=['GET', 'POST'])
def players_page(key = None):
    page = Player_info(dsn = app.config['dsn'])
    if key == 1:
        return page.open_page("name")
    elif key == 2:
        return page.open_page("surname")
    elif key == 3:
        return page.open_page("country")
    elif key == 4:
        return page.open_page("club")
    elif key == 5:
        return page.open_page("best_rating")
    elif key == 6:
        return page.open_page("best_ranking")
    elif key == 7:
        return page.open_page("best_tournament")
    elif key == 8:
        return page.open_page("best_tournament_result")
    elif key == 9:
        return page.open_page("curr_rating")
    elif key == 10:
        return page.open_page("curr_ranking")
    elif request.method == 'GET':
        return page.open_page()
    elif 'initializeTable' in request.form:
        return page.init_table()
    elif 'addplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        country = request.form['country']
        club = request.form['club']
        best_rating = request.form['best_rating']
        best_ranking = request.form['best_ranking']
        best_tournament = request.form['best_tournament']
        best_tournament_result = request.form['best_tournament_result']
        curr_rating = request.form['curr_rating']
        curr_ranking = request.form['curr_ranking']
        return page.add_player(name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking)
    elif 'deleteplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        return page.delete_player(name, surname)
    elif 'deleteplayerwithid' in request.form:
        id = request.form['id']
        return page.delete_player_with_id(id)
    elif 'findplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        return page.find_player(name, surname)
    else:
        return redirect(url_for('home_page'))

@app.route('/update_player_info/<int:key>/', methods=['GET', 'POST'])
def update_player_info_page(key = None):
    page = Player_info(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.open_update_player_info(id = key)
    elif 'updateplayer_info' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        country = request.form['country']
        club = request.form['club']
        best_rating = request.form['best_rating']
        best_ranking = request.form['best_ranking']
        best_tournament = request.form['best_tournament']
        best_tournament_result = request.form['best_tournament_result']
        curr_rating = request.form['curr_rating']
        curr_ranking = request.form['curr_ranking']
        return page.update_player_info(key, name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking)
    else:
        return redirect(url_for('home_page'))


@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)

        connection.commit()
    return redirect(url_for('home_page'))


@app.route('/rules', methods=['GET', 'POST'])
@app.route('/rules/<int:key>/', methods=['GET', 'POST'])
def rules_page(key = None):
    page = Rules(dsn = app.config['dsn'])
    if key == 1:
        return page.open_page("piece_name")
    elif key == 2:
        return page.open_page("piece_move")
    elif key == 3:
        return page.open_page("special_move")
    elif key == 4:
        return page.open_page("the_rule")
    elif key == 5:
        return page.open_page("made_by")
    elif key == 6:
        return page.open_page("date")
    elif key == 7:
        return page.open_page("name")
    elif key == 8:
        return page.open_page("capture_direction")
    elif key == 9:
        return page.open_page("starting_place")
    elif key == 10:
        return page.open_page("can_start")
    elif request.method == 'GET':
        try:
            return page.open_page()
        except:
            return page.init_table()
    elif 'initializeTable' in request.form:
        return page.init_table()
    elif 'addpiece' in request.form:
        piece_name = request.form['piece_name']
        piece_move = request.form['piece_move']
        special_move = request.form['special_move']
        return page.add_piece(piece_name, piece_move, special_move)
    elif 'addcapture' in request.form:
        name = request.form['name']
        capture_direction = request.form['capture_direction']
        starting_place = request.form['starting_place']
        can_start = request.form['can_start']
        return page.add_capture(name, capture_direction, starting_place, can_start)
    elif 'addrule' in request.form:
        the_rule = request.form['the_rule']
        made_by = request.form['made_by']
        date = request.form['date']
        return page.add_rule(the_rule, made_by, date)
    elif 'deletepiece' in request.form:
        piece_name = request.form['piece_name']
        piece_move = request.form['piece_move']
        return page.delete_piece(piece_name, piece_move)
    elif 'deleterule' in request.form:
        the_rule = request.form['the_rule']
        return page.delete_rule(the_rule)
    elif 'deletecapture' in request.form:
        name = request.form['name']
        return page.delete_capture(name)
    elif 'findpiece' in request.form:
        piece_name = request.form['piece_name']
        piece_move = request.form['piece_move']
        return page.find_pieces(piece_name, piece_move)
    elif 'findrule' in request.form:
        the_rule = request.form['the_rule']
        return page.find_rules(the_rule)
    elif 'findcapture' in request.form:
        name = request.form['name']
        return page.find_captures(name)
    else:
        return redirect(url_for('home_page'))

@app.route('/updatepiecespage/<int:key>/', methods=['GET', 'POST'])
def update_pieces_page(key = None):
    page = Rules(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.open_updatepieces(id = key)
    elif 'updatepieces' in request.form:
        piece_name = request.form['piece_name']
        piece_move = request.form['piece_move']
        special_move = request.form['special_move']
        return page.update_pieces(key, piece_name, piece_move, special_move)
    else:
        return redirect(url_for('home_page'))

@app.route('/updaterulespage/<int:key>/', methods=['GET', 'POST'])
def update_rules_page(key = None):
    page = Rules(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.open_updaterules(id = key)
    elif 'updaterules' in request.form:
        the_rule = request.form['the_rule']
        made_by = request.form['made_by']
        date = request.form['date']
        return page.update_rules(key, the_rule, made_by, date)
    else:
        return redirect(url_for('home_page'))

@app.route('/updatecapturespage/<int:key>/', methods=['GET', 'POST'])
def update_captures_page(key = None):
    page = Rules(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.open_updatecaptures(id = key)
    elif 'updatecaptures' in request.form:
        name = request.form['name']
        capture_direction = request.form['capture_direction']
        starting_place = request.form['starting_place']
        can_start = request.form['can_start']
        return page.update_captures(key, name, capture_direction, starting_place, can_start)
    else:
        return redirect(url_for('home_page'))


@app.route('/count')
def counter_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times." % count

@app.route('/localtournaments', methods=['GET', 'POST'])
@app.route('/localtournaments/<int:key>/', methods=['GET', 'POST'])
def localtour_page(key = None):
    page = Turkah(dsn = app.config['dsn'])
    if key == 1:
        return page.open_page("name")
    elif key == 2:
        return page.open_page("surname")
    elif key == 3:
        return page.open_page("win DESC")
    elif key == 4:
        return page.open_page("lose DESC")
    elif key == 5:
        return page.open_page("draw DESC")
    elif request.method == 'GET':
        try:
            return page.open_page()
        except:
            return page.init_table()
    elif 'initializeTable' in request.form:
        return page.init_table()
    elif 'addplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        win = request.form['win']
        lose = request.form['lose']
        draw = request.form['draw']
        return page.add_player(name, surname, win, lose, draw)
    elif 'addgame' in request.form:
        playerone = request.form['playerone']
        playertwo = request.form['playertwo']
        result = request.form['result']
        return page.add_game(playerone, playertwo, result)
    elif 'deleteplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        return page.delete_player(name, surname)
    elif 'deleteplayerwithid' in request.form:
        id = request.form['id']
        return page.delete_player_with_id(id)
    elif 'deletegame' in request.form:
        id = request.form['id']
        return page.delete_game(id)
    elif 'findplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        return page.find_player(name, surname)
    elif 'findplayerwithid' in request.form:
        id = request.form['id']
        return page.find_player_with_id(id)
    elif 'findgamebyid' in request.form:
        id = request.form['id']
        return page.find_game_by_id(id)
    elif 'findgamebyplayer' in request.form:
        id = request.form['id']
        return page.find_game_by_player(id)
    else:
        return redirect(url_for('home_page'))

@app.route('/updatelp/<int:key>/', methods=['GET', 'POST'])
def updatelp_page(key = None):
    page = Turkah(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.open_updatelp(id = key)
    elif 'updateplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        win = request.form['win']
        lose = request.form['lose']
        draw = request.form['draw']
        return page.update_player(key, name, surname, win, lose, draw)
    else:
        return redirect(url_for('home_page'))

@app.route('/updatelg/<int:key>/', methods=['GET', 'POST'])
def updatelg_page(key = None):
    page = Turkah(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.open_updatelg(id = key)
    elif 'updategame' in request.form:
        playerone = request.form['playerone']
        playertwo = request.form['playertwo']
        result = request.form['result']
        return page.update_game(key, playerone, playertwo, result)
    else:
        return redirect(url_for('home_page'))

@app.route('/upcoming_events', methods=['GET', 'POST'])
def upcoming_events():
    page = event(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.open_page()
    elif 'initializeTable' in request.form:
        return page.init_table()
    elif 'addevent' in request.form:
        date = request.form['date']
        place = request.form['place']
        player1 = request.form['player1']
        player2 = request.form['player2']
        return page.addevent(date, place, player1, player2)
    elif 'deleteevent' in request.form:
        number = request.form['number']
        return page.deleteevent(number)
    elif 'deleteevent1' in request.form:
        date = request.form['date']
        place = request.form['place']
        return page.delete_event(date, place)
    elif 'findevent' in request.form:
        number = request.form['number']
        return page.find_event(number)
    elif 'findevent1' in request.form:
        date = request.form['date']
        place = request.form['place']
        return page.find_event_name(date, place)
    else:
        return redirect(url_for('home_page'))

@app.route('/history', methods=['GET', 'POST'])
def history():
    page = facts(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.open_page()
    elif 'initializeTable' in request.form:
        return page.init_table()
    elif 'addfact' in request.form:
        date = request.form['date']
        place = request.form['place']
        fact = request.form['fact']
        return page.addfact(date, place, fact)
    elif 'deletefact' in request.form:
        number = request.form['number']
        return page.deletefact(number)
    elif 'deletefact1' in request.form:
        date = request.form['date']
        place = request.form['place']
        return page.delete_fact(date, place)
    elif 'updaterfact' in request.form:
        date = request.form['date']
        place = request.form['place']
        fact = request.form['fact']
        return page.update_rules(date, place, fact)
    elif 'findfact' in request.form:
        number = request.form['number']
        return page.findfact(number)
    elif 'findfact1' in request.form:
        date = request.form['date']
        place = request.form['place']
        return page.find_fact(date, place)
    else:
        return redirect(url_for('home_page'))




if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)

