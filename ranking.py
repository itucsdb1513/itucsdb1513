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

            query = """SELECT * FROM worldplayers ORDER BY %s"""% sort
            cursor.execute(query)
            players = cursor.fetchall()

            query = """SELECT * FROM countries_table
                        ORDER BY %s"""% sort
            cursor.execute(query)
            countries = cursor.fetchall()
        return render_template('rankings.html', players = players, countries = countries)



    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS worldplayers CASCADE;
                       DROP TABLE IF EXISTS countries_table CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE countries_table (
                        id serial PRIMARY KEY,
                        country_name text UNIQUE NOT NULL,
                        average integer DEFAULT 0,
                        gm integer DEFAULT 0,
                        im integer DEFAULT 0,
                        total_titled integer DEFAULT 0,
                        total_top integer DEFAULT 0,
                        country_rank integer DEFAULT 0,
                        best_player text UNIQUE NOT NULL,
                        highest_rating integer DEFAULT 0);


                        CREATE TABLE worldplayers (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        surname text NOT NULL,
                        country text NOT NULL REFERENCES countries_table(country_name) ON UPDATE CASCADE ON DELETE RESTRICT,
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
                        ('SHAKHRIYAR', 'MAMMADYAROV', 'AZERBAIJAN', 'SOCAR BAKU', 2746, 20, 30, 'MALE');

                        INSERT INTO countries_table (country_name, average, gm, im, total_titled, total_top, country_rank, best_player, highest_rating)
                        VALUES
                        ('RUSSIA', 2740, 231, 522, 2390, 24, 1, 'Vladimir Kramnik', 2796),
                        ('CHINA', 2714, 37, 31, 143, 7, 2, 'Liren Ding', 2776),
                        ('UKRAINE', 2690, 87, 198, 523, 9, 3, 'Pavel Eljanov', 2763),
                        ('AZERBAIJAN', 2645, 24, 22, 120, 3, 9, 'Shakhriyar Mamedyarov', 2748),
                        ('NORWAY', 2564, 11, 31, 118, 1, 23, 'Magnus Carlsen', 2834)"""
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

    def add_country(self, country_name, average, gm, im, total_titled, total_top, country_rank, best_player, highest_rating):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO countries_table (country_name, average, gm, im, total_titled, total_top, country_rank, best_player, highest_rating)
                        VALUES
                        ('%s', %s, %s, %s, %s, %s, %s, '%s', %s )""" % (country_name, average, gm, im, total_titled, total_top, country_rank, best_player, highest_rating)
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

    def delete_country(self, country_name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM countries_table WHERE country_name = '%s'""" % (country_name)
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

    def open_updatecountries(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM countries_table WHERE id  = %s" % (id)
            cursor.execute(query)
            countries = cursor.fetchone()
        return render_template('updatecountriespage.html', countries = countries)

    def update_player(self, id, name, surname, country, club, rating, ranking, age, gender):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE worldplayers
                        SET name = '%s', surname = '%s', country = '%s', club = '%s', rating = '%s', ranking = '%s', age = '%s', gender = '%s'
                        WHERE id = %s""" % (name, surname, country, club, rating, ranking, age, gender, id)
            cursor.execute(query)
        return redirect(url_for('rankings_page'))

    def update_countries(self, id, country_name, average, gm, im, total_titled, total_top, country_rank, best_player, highest_rating):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE countries_table
                        SET country_name = '%s', average = %s, gm = %s, im = %s, total_titled = %s, total_top = %s,
                            country_rank = %s, best_player = '%s', highest_rating = %s
                        WHERE id = %s""" % (country_name, average, gm, im, total_titled, total_top, country_rank, best_player, highest_rating, id)
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

    def find_country(self, country_name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM countries_table
                        WHERE country_name LIKE '%s%%'
                        ORDER BY id """ % (country_name)
            cursor.execute(query)
            countries = cursor.fetchall()
        return render_template('findcountries.html', countries = countries)

