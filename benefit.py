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
                        Name text UNIQUE NOT NULL,
                        HasBenefit text UNIQUE NOT NULL references benefit(Benef)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE)"""
            cursor.execute(query)

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people= cursor.fetchall()

            query = """CREATE TABLE IF NOT EXISTS relation (
                        id serial PRIMARY KEY,
                        ThePeople text NOT NULL references  people(Name)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                        TheBenefit text NOT NULL references  benefit(Benef)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                        duration text)"""
            cursor.execute(query)

            query = "SELECT ThePeople,TheBenefit,duration FROM relation"
            cursor.execute(query)
            relation= cursor.fetchall()

            cursor.close()
        return render_template('benefit.html', benefit = benefit,people=people,relation=relation)

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
                        ('Improving Intelligence','Logical'),
                         ('Deep Thinking','Logical'),
                         ('Critical Thinking','Logical'),
                         ('Calmness','Psychological'),
                         ('Charisma','Behavioral'),
                         ('Patience','Psychological'),
                         ('Farsightedness','Psychological')"""
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
                        Name text UNIQUE NOT NULL,
                        HasBenefit text NOT NULL references benefit(Benef)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE) """
            cursor.execute(query)

            query = """INSERT INTO people (Name,HasBenefit)
                        VALUES
                        ( 'Ali','Improving Intelligence' ),
                         ('Veli','Deep Thinking'),
                         ('Mehmet','Patience'),
                         ('Umut','Charisma'),
                         ('Can','Critical Thinking'),
                         ('Mustafa','Calmness'),
                         ('Berke','Farsightedness')"""
            cursor.execute(query)


            cursor.close()
        return redirect(url_for('benefit_page'))

    def init_table3(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS relation CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS relation (
                        id serial PRIMARY KEY,
                        ThePeople text NOT NULL references  people(Name)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                        TheBenefit text NOT NULL references  benefit(Benef)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                        duration text)"""
            cursor.execute(query)


            query = """INSERT INTO relation (ThePeople,TheBenefit,duration)
                        VALUES
                        ('Ali',  'Improving Intelligence','Long Term'),
                         ('Veli','Deep Thinking','Temporary'),
                         ('Mehmet','Patience','Permanent'),
                         ('Umut','Charisma','Short Term'),
                         ('Can','Critical Thinking','Long Term'),
                         ('Mustafa','Calmness','Short Term'),
                         ('Berke','Farsightedness','Temporary')"""
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

    def addrelation(self, ThePeople,TheBenefit,duration):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO relation (ThePeople,TheBenefit,duration)
                        VALUES
                        ('%s', '%s','%s')""" % (ThePeople,TheBenefit,duration)
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

    def deleterelation(self, ThePeople):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM relation WHERE ThePeople = '%s' """ % (ThePeople)
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

            query = "SELECT ThePeople,TheBenefit,duration FROM relation"
            cursor.execute(query)
            relation= cursor.fetchall()

            query = """SELECT Name,HasBenefit FROM people
                        WHERE Name = '%s'""" % (Name)

            cursor.execute(query)
            result2=cursor.fetchall()
            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people,result2=result2,relation=relation)

    def findpeoplebybenefit(self, HasBenefit):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT Benef ,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people = cursor.fetchall()

            query = "SELECT ThePeople,TheBenefit,duration FROM relation"
            cursor.execute(query)
            relation= cursor.fetchall()

            query = """SELECT Name,HasBenefit FROM people
                        WHERE HasBenefit = '%s'""" % (HasBenefit)

            cursor.execute(query)
            result2=cursor.fetchall()
            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people,result2=result2,relation=relation)

    def findbenefit(self, Benef):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT Benef ,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people = cursor.fetchall()

            query = "SELECT ThePeople,TheBenefit,duration FROM relation"
            cursor.execute(query)
            relation= cursor.fetchall()

            query = """SELECT Benef, Type FROM benefit
                        WHERE Benef = '%s'""" % (Benef)

            cursor.execute(query)
            result=cursor.fetchall()
            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people,result=result,relation=relation)

    def findbenefitbytype(self, Type):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT Benef ,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people = cursor.fetchall()

            query = "SELECT ThePeople,TheBenefit,duration FROM relation"
            cursor.execute(query)
            relation= cursor.fetchall()

            query = """SELECT Benef, Type FROM benefit
                        WHERE Type = '%s'""" % (Type)

            cursor.execute(query)
            result=cursor.fetchall()
            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people,result=result,relation=relation)

    def findrelation(self,ThePeople):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT Benef ,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people = cursor.fetchall()

            query = "SELECT ThePeople,TheBenefit,duration FROM relation"
            cursor.execute(query)
            relation= cursor.fetchall()

            query = """SELECT ThePeople,TheBenefit,duration FROM relation
                        WHERE ThePeople = '%s'""" % (ThePeople)

            cursor.execute(query)
            result3=cursor.fetchall()
            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people,result3=result3,relation=relation)

    def findrelationbyduration(self,duration):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT Benef ,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people = cursor.fetchall()

            query = "SELECT ThePeople,TheBenefit,duration FROM relation"
            cursor.execute(query)
            relation= cursor.fetchall()

            query = """SELECT ThePeople,TheBenefit,duration FROM relation
                        WHERE duration = '%s'""" % (duration)

            cursor.execute(query)
            result3=cursor.fetchall()
            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people,result3=result3,relation=relation)

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

            query = "SELECT ThePeople,TheBenefit,duration FROM relation"
            cursor.execute(query)
            relation= cursor.fetchall()

            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people,relation=relation)

    def updatepeople(self,Name,new,new2):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE people
                        SET Name= '%s',
                            HasBenefit='%s'
                             WHERE Name = '%s' """ % (new,new2,Name)
            cursor.execute(query)

            query = "SELECT Benef,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people = cursor.fetchall()

            query = "SELECT ThePeople,TheBenefit,duration FROM relation"
            cursor.execute(query)
            relation= cursor.fetchall()

            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people,relation=relation)

    def updaterelation(self,ThePeople,new,new2,new3):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE relation
                        SET TheBenefit= '%s',
                            duration= '%s',
                            ThePeople='%s'
                             WHERE ThePeople = '%s' """ % (new,new2,new3,ThePeople)
            cursor.execute(query)

            query = "SELECT Benef,Type FROM benefit"
            cursor.execute(query)
            benefit = cursor.fetchall()

            query = "SELECT Name,HasBenefit FROM people"
            cursor.execute(query)
            people = cursor.fetchall()

            query = "SELECT ThePeople,TheBenefit,duration FROM relation"
            cursor.execute(query)
            relation= cursor.fetchall()

            cursor.close()
        return render_template('benefit.html',benefit=benefit,people=people,relation=relation)
