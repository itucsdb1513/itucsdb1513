import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class Ranking:
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def open_page(self, sort = "id"):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS worldplayers (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        surname text NOT NULL,
                        country text NOT NULL,
                        club text NOT NULL,
                        rating integer DEFAULT 0,
                        ranking integer DEFAULT 0,
                        age integer DEFAULT 0,
                        gender text NOT NULL)"""
            cursor.execute(query)

            query = """SELECT * FROM worldplayers ORDER BY %s""" % sort
            cursor.execute(query)
            players = cursor.fetchall()
        return render_template('rankings.html', players = players)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS worldplayers CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE worldplayers (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        surname text NOT NULL,
                        country text NOT NULL,
                        club text NOT NULL,
                        rating integer DEFAULT 0,
                        ranking integer DEFAULT 0,
                        age integer DEFAULT 0,
                        gender text NOT NULL,
                        UNIQUE (name, surname))"""
            cursor.execute(query)

            query = """INSERT INTO worldplayers (name, surname, country, club, rating, ranking, age, gender)
                        VALUES
                        ('MAGNUS', 'CARLSEN', 'NORWAY', 'OS BADEN BADEN', 2850, 1, 25, 'MALE'),
                        ('TEYMOUR', 'RADJABOV', 'AZERBAIJAN', 'SOCAR BAKU', 2739, 22, 28, 'MALE'),
                        ('SHAKHRIYAR', 'MAMMADYAROV', 'AZERBAIJAN', 'SOCAR BAKU', 2746, 20, 30, 'MALE')"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rankings_page'))

    def add_player(self, name, surname, country, club, rating, ranking, age, gender):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO worldplayers (name, surname, country, club, rating, ranking, age, gender)
                        VALUES
                        ('%s', '%s', '%s', '%s', %s, %s, %s, '%s')""" % (name, surname, country, club, rating, ranking, age, gender)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rankings_page'))

    def delete_player(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM worldplayers WHERE name = '%s'
                        AND surname = '%s' """ % (name, surname)
            cursor.execute(query)
            connection.commit()

        return redirect(url_for('rankings_page'))

    def delete_player_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM worldplayers WHERE id = '%s' """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rankings_page'))

    def open_update_player(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM worldplayers WHERE id  = %s" % (id)
            cursor.execute(query)
            player = cursor.fetchone()
            return render_template('update_player.html', player = player)

    def update_player(self, id, name, surname, country, club, rating, ranking, age, gender):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE worldplayers
                        SET name = '%s', surname = '%s', country = '%s', club = '%s', rating = '%s', ranking = '%s', age = '%s', gender = '%s'
                        WHERE id = %s""" % (name, surname, country, club, rating, ranking, age, gender, id)
            cursor.execute(query)
        return redirect(url_for('rankings_page'))

    def find_player(self, name, surname):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM worldplayers
                        WHERE name LIKE '%s%%'
                          AND surname LIKE '%s%%'
                        ORDER BY id """ % (name, surname)
            cursor.execute(query)
            player = cursor.fetchall()
        return render_template('find_player.html', player = player)
