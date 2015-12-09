import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for


class Player_info:
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def open_page(self, sort = "id"):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM player_info ORDER BY %s""" % sort
            cursor.execute(query)
            player_info = cursor.fetchall()
        return render_template('player_info.html', player_info = player_info)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS player_info"""
            cursor.execute(query)

            query = """CREATE TABLE player_info (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        surname text NOT NULL,
                        country text NOT NULL,
                        club text NOT NULL,
                        best_rating integer DEFAULT 0,
                        best_ranking integer DEFAULT 0,
                        best_tournament text NOT NULL,
                        best_tournament_result text NOT NULL,
                        curr_rating integer DEFAULT 0,
                        curr_ranking integer DEFAULT 0)"""
            cursor.execute(query)

            query = """INSERT INTO player_info (name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking)
                        VALUES
                        ('MAGNUS', 'CARLSEN', 'NORWAY', 'OS BADEN BADEN', 2850 , 1, 'MonteCarlo', 'Champion', 2850, 1),
                        ('TEYMOUR', 'RADJABOV', 'AZERBAIJAN','SOCAR BAKU', 2760, 8, 'Lenaries','finalist', 2739, 22),
                        ('SHAKHRIYAR', 'MAMMADYAROV', 'AZERBAIJAN', 'SOCAR BAKU',2755, 12,'Australian Open', 'Finalist' ,2746, 20)"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('players_page'))



    def add_player(self, name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO player_info (name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking)
                        VALUES
                        ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('players_page'))

    def delete_player(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM player_info WHERE name = '%s'
                        AND surname = '%s' """ % (name, surname)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('players_page'))

    def open_update_player_info(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM player_info WHERE id  = %s" % (id)
            cursor.execute(query)
            player_info = cursor.fetchone()
        return render_template('update_biography.html', player_info = player_info)

    def update_player_info(self, id, name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE player_info
                        SET name = '%s', surname = '%s', country = '%s', club = '%s', best_rating = '%s',
                             best_ranking = '%s', best_tournament = '%s', best_tournament_result = '%s',
                             curr_rating = '%s', curr_ranking = '%s'
                        WHERE id = %s""" % (name, surname, country, club, best_rating, best_ranking, best_tournament, best_tournament_result, curr_rating, curr_ranking, id)

            cursor.execute(query)

        return redirect(url_for('players_page'))

    def find_player(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM player_info
                        WHERE name LIKE '%s%%'
                          AND surname LIKE '%s%%'
                        ORDER BY id """ % (name, surname)
            cursor.execute(query)
            player_info = cursor.fetchall()
        return render_template('find_playerBiography.html', player_info = player_info)
