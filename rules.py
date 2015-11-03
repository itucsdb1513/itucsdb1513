import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class Rules:
    def __init__(self, dsn):
        self.dsn = dsn
        return

    def open_page(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS pieces (
                        id serial PRIMARY KEY,
                        piece_name text NOT NULL,
                        piece_rule text NOT NULL,
                        special_move text NOT NULL)"""
            cursor.execute(query)

            query = "SELECT * FROM pieces"
            cursor.execute(query)
            rules = cursor.fetchall()
        return render_template('rules.html', rules = rules)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS pieces"""
            cursor.execute(query)

            query = """CREATE TABLE pieces (
                        id serial PRIMARY KEY,
                        piece_name text NOT NULL,
                        piece_rule text NOT NULL,
                        special_move text NOT NULL)"""
            cursor.execute(query)

            query = """INSERT INTO pieces (piece_name, piece_rule, special_move)
                        VALUES
                        ('King', 'Hori.,Ver.', 'Castling'),
                        ('Queen', 'H, V, Diagn.', ' ')"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def add_piece(self, piece_name, piece_rule, special_move):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO pieces (piece_name, piece_rule, special_move)
                        VALUES
                        ('%s', '%s', '%s')""" % (piece_name, piece_rule, special_move)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def delete_piece(self, piece_name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM pieces WHERE piece_name = '%s' """ % (piece_name)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))

    def delete_piece_with_id(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM pieces WHERE id = '%s' """ % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('rules_page'))
