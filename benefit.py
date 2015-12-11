import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask.helpers import url_for

class Benefit:
    def __init__(self, dsn):
        self.dsn = dsn;

    def open_page(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS benefit (
                        ID serial PRIMARY KEY,
                        Benef text UNIQUE NOT NULL,
                        Type text NOT NULL)"""
            cursor.execute(query)

            query = "SELECT Benef,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = """CREATE TABLE IF NOT EXISTS people (
                        Peopleid serial PRIMARY KEY,
                        Name text NOT NULL,
                        HasBenefit text NOT NULL references benefit(Benef)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE)"""
            cursor.execute(query)

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people= cursor.fetchall()
            cursor.close()
        return render_template('benefit.html', benefit = benefit,people=people)

    def init_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS benefit CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE benefit (
                        ID serial PRIMARY KEY,
                        Benef text UNIQUE NOT NULL,
                        Type text NOT NULL)"""
            cursor.execute(query)

            query = """INSERT INTO benefit (Benef,Type)
                        VALUES
                        ('improving intelligence',  'Logical'),
                         ('dasdasd','asdasdas')"""
            cursor.execute(query)


            cursor.close()
        return redirect(url_for('benefit_page'))


    def init_table2(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS people CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS people (
                        Peopleid serial PRIMARY KEY,
                        Name text NOT NULL,
                        HasBenefit text NOT NULL references benefit(Benef)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE) """
            cursor.execute(query)

            query = """INSERT INTO people (Name,HasBenefit)
                        VALUES
                        ( 'Logical','improving intelligence' ),
                         ('asdasdas','dasdasd')"""
            cursor.execute(query)


            cursor.close()
        return redirect(url_for('benefit_page'))



    def addbenefit(self, Benef,Type):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO benefit (Benef,Type)
                        VALUES
                        ('%s', '%s')""" % (Benef,Type)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('benefit_page'))

    def addpeople(self, Name,HasBenefit):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO people (Name,HasBenefit)
                        VALUES
                        ('%s', '%s')""" % (Name,HasBenefit)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('benefit_page'))


    def deletepeople(self, Name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM people WHERE Name = '%s' """ % (Name)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('benefit_page'))


    def deletebenefit(self, Benef):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM benefit WHERE Benef = '%s' """ % (Benef)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('benefit_page'))

    def findpeople(self, Name):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT Benef ,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people = cursor.fetchall()

            query = """SELECT Name,HasBenefit FROM people
                        WHERE Name = '%s'""" % (Name)

            cursor.execute(query)
            result2=cursor.fetchall()
            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people,result2=result2)

    def findbenefit(self, Benef):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT Benef ,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people = cursor.fetchall()

            query = """SELECT Benef, Type FROM benefit
                        WHERE Benef = '%s'""" % (Benef)

            cursor.execute(query)
            result=cursor.fetchall()
            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people,result=result)


    def updatebenefit(self, Benef,new,new2):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE benefit
                        SET Benef= '%s',
                            Type = '%s'
                             WHERE Benef = '%s' """ % (new,new2,Benef)
            cursor.execute(query)

            query = "SELECT Benef,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people = cursor.fetchall()

            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people)

    def updatepeople(self,Name,new):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE people
                        SET Name= '%s'
                             WHERE Name = '%s' """ % (new,Name)
            cursor.execute(query)

            query = "SELECT Benef,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people = cursor.fetchall()

            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people)
