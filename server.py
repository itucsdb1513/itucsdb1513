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

@app.route('/rankings')
def rankings_page():
    player1 = Player('Magnus', 'Carlsen', 'Norway', 'OS Baden Baden', '2850', '1', '25', 'male')
    player2 = Player('Teymour', 'Radjabov', 'Azerbaijan', 'SOCAR BAKU', '2739', '22', '28', 'male')
    players = [(1, player1), (2, player2)]
    now = datetime.datetime.now()
    return render_template('rankings.html', players = players, current_time = now.ctime())


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
def localtour_page():
    page = Turkah(dsn = app.config['dsn'])
    if request.method == 'GET':
        return page.open_page()
    elif 'initializeTable' in request.form:
        return page.init_table()
    elif 'addplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        win = request.form['win']
        lose = request.form['lose']
        return page.add_player(name, surname, win, lose)
    elif 'deleteplayer' in request.form:
        name = request.form['name']
        surname = request.form['surname']
        return page.delete_player(name, surname)
    elif 'deleteplayerwithid' in request.form:
        id = request.form['id']
        return page.delete_player_with_id(id)
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
        return page.delete_event(number)
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