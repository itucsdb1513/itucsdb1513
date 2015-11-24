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
def rankings_page():
    page = Ranking(dsn = app.config['dsn'])
    if request.method == 'GET':
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
def rules_page():
    page = Rules(dsn = app.config['dsn'])
    if request.method == 'GET':
        try:
            return page.open_page()
        except:
            return page.init_table()
    elif 'initializeTable' in request.form:
        return page.init_table()
    elif 'addpiece' in request.form:
        piece_name = request.form['piece_name']
        piece_rule = request.form['piece_rule']
        special_move = request.form['special_move']
        return page.add_piece(piece_name, piece_rule, special_move)
    elif 'addrule' in request.form:
        the_rule = request.form['the_rule']
        made_by = request.form['made_by']
        date = request.form['date']
        return page.add_rule(the_rule, made_by, date)
    elif 'deletepiece' in request.form:
        piece_name = request.form['piece_name']
        return page.delete_piece(piece_name)
    elif 'deletepiecewithid' in request.form:
        id = request.form['id']
        return page.delete_piece_with_id(id)
    elif 'deleterule' in request.form:
        the_rule = request.form['the_rule']
        return page.delete_rule(the_rule)
    elif 'deleterulewithid' in request.form:
        id = request.form['id']
        return page.delete_rule_with_id(id)
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

