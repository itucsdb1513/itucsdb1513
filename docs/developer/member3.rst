Parts Implemented by Ira Shyti
==============================
Upcoming Events table
---------------------
This table shows the future events of the main chess championships.
The table has six columns. The primary key of the table is the number, which is generated serially.
The table has a foreign key. The championships attribute is referenced from champsionships attribute of champioships table.
The attribute date is unique.

+--------------+--------+----------+-------------+-----------+
| Attribuite   | Type   | Not Null | Primary key | Reference |
+==============+========+==========+=============+===========+
| number       | serial | 1        | Yes         | No        |
+--------------+--------+----------+-------------+-----------+
| date         | text   | 1        | No          | No        |
+--------------+--------+----------+-------------+-----------+
| place        | text   | 1        | No          | No        |
+--------------+--------+----------+-------------+-----------+
| player1      | text   | 1        | No          | No        |
+--------------+--------+----------+-------------+-----------+
| player2      | text   | 1        | No          | No        |
+--------------+--------+----------+-------------+-----------+
| championship | text   | 1        | No          | Yes       |
+--------------+--------+----------+-------------+-----------+

   - *number* is the primary key
   - *date hold* the date of the event
   - *place* is the city where the event will take place
   - *player1* holds name of player 1
   - *player2* holds name of player 2
   - *championship* shows to which championship this event belongs

**SQL statement for initializing the upcoming events table : **

.. code-block:: python

     query = """CREATE TABLE IF NOT EXISTS events (
                        number serial PRIMARY KEY,
                        date text UNIQUE NOT NULL,
                        place text NOT NULL,
                        player1 text NOT NULL,
                        player2 text NOT NULL,
                        champ text NOT NULL)"""
            cursor.execute(query)

Initiale table
++++++++++++++
The upcoming events table can be initialized by pressing the *initialize table* button that is above the table.
When the table is initialized it shows eight events.

**SQL statement for initializing the upcoming events table :**

.. code-block:: python

   query = """INSERT INTO events (date, place, player1, player2, champ)
                        VALUES
                        ('3.November', 'Tiran', 'Ira', 'Rei', 'Albanian'),
                        ('16.May', 'Munchen', 'Kim', 'Rus', 'World'),
                        ('4.December', 'Istanbul', 'Javid', 'Ahmet', 'Turkish'),
                        ('10.December', 'Ankara', 'Mursit', 'Soner', 'European'),
                        ('10.January', 'London', 'Jack', 'John', 'English'),
                        ('23.February', 'Rome', 'Anna', 'Maria', 'Italian'),
                        ('19.June', 'Madrid', 'Juan', 'Ken', 'European'),
                        ('15.May', 'Berlin', 'Mehmet', 'Elif', 'World')"""
            cursor.execute(query)
            connection.commit()


Add Event
+++++++++
Every user can add an event into the table. User should give values for all the attributes since none of them can be empty.
While adding a new event, the user should take in considerance that the new event can not have the same date with any other
event in the table since the date attribute is unique. Also user should take in considerance that only events of championships
that are part of *championship* table can be added since the championship attribute has a reference from that table.

**SQL statement for aadding an event to the table :**

.. code-block:: python

   def addevent(self, date, place, player1, player2, champ):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO events (date, place, player1, player2, champ)
                        VALUES
                        ('%s', '%s', '%s', '%s', '%s')""" % (date, place, player1, player2, champ)
            cursor.execute(query)
            cursor.close()
        return redirect(url_for('upcoming_events'))

Find Event
++++++++++
For the upcoming events table there are three ways in which user can find an event. First way is to find
it by the number on the table. Second way is to find it by entering the date and the place of the even. The last way is
to find the event baseed on the championship it belongs. In this way all the events of that championship will be listed.

**SQL statement for finding event by the number on the table :**

.. code-block:: python

   def find_event(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM events WHERE number = %s """ % (number)
            cursor.execute(query)
            events = cursor.fetchall()
            cursor.close()
        return render_template('findevent.html', events = events)

**SQL statement for finding event by date and place :**

.. code-block:: python

   def find_event_name(self, date, place):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM events
                        WHERE date LIKE '%s%%'
                          AND place LIKE '%s%%'
                        ORDER BY number """ % (date, place)
            cursor.execute(query)
            events = cursor.fetchall()
            cursor.close()
        return render_template('findevent.html', events = events)

**SQL statement for finding event by championship :**

.. code-block:: python

   def find_event_2(self, champ):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM events
                         WHERE champ ='%s' """ % (champ)
            cursor.execute(query)
            events = cursor.fetchall()
            cursor.close()
        return render_template('findevent.html', events = events)

Delete Event
++++++++++++
The user can choose one of the three ways for deleting an event from the table.
They can delete an event by its number, by the date and place, or by the name of the championship it is part of. The
user should take in considerance that when he/she chooses to delete an event by its championship, all the events in the table
 that are part of that championship will be deleted.

**SQL statement for deleting an event by the number on the table :**

.. code-block:: python

   def deleteevent(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM events WHERE number = '%s' """ % (number)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('upcoming_events'))



**SQL statement for deleting an event by the date and place :**

.. code-block:: python

   def delete_event(self, date, place):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM events WHERE date = '%s'
                        AND place = '%s' """ % (date, place)
            cursor.execute(query)

**SQL statement for deleting an event by the championship :**

.. code-block:: python

   def deleteevent_2(self, champ):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM events WHERE champ = '%s' """ % (champ)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('upcoming_events'))

Update Event
++++++++++++
An event can be updated by pressing the update button which is located at the rightmost column in the row of the event that
the user wants to update. While updating an event the user should be careful not to change the value of *championship*
attribute since it is referenced to another table.

**SQL statement for opening the  update event page :**

.. code-block:: python

   def open_updatetour(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM tours WHERE number  = %s" % (number)
            cursor.execute(query)
            tour_up = cursor.fetchone()
        return render_template('updatetour.html', tour_up = tour_up)


**SQL statement for updating an event :**

.. code-block:: python

   def update_event(self, number, date, place, player1, player2, champ):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE events
                        SET date = '%s', place = '%s', player1 = '%s', player2 = '%s',
                            champ = '%s'
                        WHERE number = %s""" % (date, place, player1, player2, champ, number)
            cursor.execute(query)
        return redirect(url_for('upcoming_events'))


Championships Table
-------------------
This table shows the chess championships in the world. It has five attributes which are number, championship, year,
players, games. The primary key of this table is number which is serially generated. Championship is a foreign key for the
upcoming events table and because of this it is unique. Year shows the year the championship will happen. Players refers to
the total number of chess players to that championship and games is for the total number of games that will occur in the
championship.


+--------------+---------+----------+-------------+-----------+
| Attribuite   | Type    | Not Null | Primary key | Reference |
+==============+=========+==========+=============+===========+
| number       | serial  | 1        | Yes         | No        |
+--------------+---------+----------+-------------+-----------+
| championship | text    | 1        | No          | Ye        |
+--------------+---------+----------+-------------+-----------+
| year         | integer | 1        | No          | No        |
+--------------+---------+----------+-------------+-----------+
| players      | integer | 1        | No          | No        |
+--------------+---------+----------+-------------+-----------+
| games        | integer | 1        | No          | No        |
+--------------+---------+----------+-------------+-----------+

   - *number* is the primary key
   - *championship* (cha) holds the name of championship
   - *year* is the year the championship will happen
   - *players* is the total number of players in that championship
   - *games* total number of games that will be played


**SQL statement for initializing the upcoming events table :**

.. code-block:: python


   query = """CREATE TABLE tours (
                        number serial PRIMARY KEY,
                        cha  text UNIQUE NOT NULL,
                        year integer NOT NULL,
                        players integer NOT NULL,
                        games integer NOT NULL)"""
            cursor.execute(query)


Initialize table
++++++++++++++++
User can initialize the championships table to its initiall values by pressing the initialize table button.
When the table is initialized it shows the information for seven different championships.

**SQL statement for initializing the upcoming events table :**

.. code-block:: python

   query = """INSERT INTO tours (cha, year, players, games)
                        VALUES
                        ('World', 2016, 24, 72),
                        ('European', 2017, 16, 36),
                        ('Asian', 2016, 16, 36),
                        ('Albanian', 2016, 16, 36),
                        ('English', 2016, 20, 68),
                        ('Italian', 2016, 14, 3),
                        ('Turkish', 2016, 16, 36)"""
            cursor.execute(query)


Add Championship
++++++++++++++++
The users can add an new championship on the table by entering all the values that are required since none of them can be
NULL. User should take in considerance that if a championship already exists on the table, no other championship with same
name can be added in the table.

**SQL statement for adding a championship :**

.. code-block:: python

   def addtour(self, cha, year, players, games):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO tours (cha, year, players, games)
                        VALUES
                        ('%s', %s, %s, %s)""" % (cha, year, players, games)
            cursor.execute(query)
            cursor.close()
        return redirect(url_for('upcoming_events'))


Find Championship
+++++++++++++++++
There are two ways by which a user can find a championship, either by its number on the table or by the name of the
 championship.

 **SQL statement for finding championship by the number on the table :**

.. code-block:: python

   def find_tour(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM tours WHERE number = %s """ % (number)
            cursor.execute(query)
            tours = cursor.fetchall()
            cursor.close()
        return render_template('find_tour.html', tours = tours)

 **SQL statement for finding event by championship name :**

.. code-block:: python

   def find_tour_name(self, cha):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM tours
                        WHERE cha LIKE '%s%%'
                        ORDER BY number """ % (cha)
            cursor.execute(query)
            tours = cursor.fetchall()
            cursor.close()
        return render_template('find_tour.html', tours = tours)


Delete Championship
+++++++++++++++++++
There are also two ways for deleting a championship, which are same ways used to find it. The user should take in
considerance that this table is connected with the upcoming events table by a foreing key. The foreign key restricts
the user to delete a championship if in the events table there is any event part of this championship. If there is no such
event in the upcoming events table, than the user can delete the championship.

 **SQL statement for deleting championship by the number on the table :**

.. code-block:: python

   def deletetour(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM tours WHERE number = '%s' """ % (number)
            cursor.execute(query)
            cursor.close()
        return redirect(url_for('upcoming_events'))



 **SQL statement for deleting championship by its name :**

.. code-block:: python

   def delete_tour(self, cha):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM tours WHERE cha = '%s'
                         """ % (cha)
            cursor.execute(query)
            cursor.close()
        return redirect(url_for('upcoming_events'))



Update Championship
+++++++++++++++++++
The user can update a championshi by clicking on its name. The user shouldtake inconsiderance that he/she cannot changethe
 name of a championship that has an event in the upcoming events table.

 **SQL statement for updating championship :**

.. code-block:: python

   def tour_update(self, number, cha, year, players, games):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE tours
                        SET cha = '%s', year = %s, players =%s,
                            games = %s
                        WHERE number = %s""" % (cha, year, players, games, number)
            cursor.execute(query)
        return redirect(url_for('upcoming_events'))



History of chess table
----------------------

This table is created to inform the users about the history of chess. The table has four columns. The primary key of the table
is the number, which is gennerated serially. This is a simple table and does not have any foreign key.

+------------+--------+----------+-------------+-----------+
| Attribuite | Type   | Not Null | Primary key | Reference |
+============+========+==========+=============+===========+
| number     | serial | 1        | Yes         | No        |
+------------+--------+----------+-------------+-----------+
| date       | text   | 1        | No          | No        |
+------------+--------+----------+-------------+-----------+
| place      | text   | 0        | No          | No        |
+------------+--------+----------+-------------+-----------+
| fact       | text   | 1        | No          | No        |
+------------+--------+----------+-------------+-----------+

   - *number* is the primary key
   - *date* holds the date of the historical fact
   - *place* is the place that an historical event happened
   - *fact* hold the histroical information


**SQL statement for initializing the upcoming events table :**

.. code-block:: python

   query = """CREATE TABLE IF NOT EXISTS history (
                        number serial PRIMARY KEY,
                        date text NOT NULL,
                        place text ,
                        fact text NOT NULL)"""
            cursor.execute(query)

Initialize table
++++++++++++++++
The history table can be initialize by pressing the *initialize table* button. When table is initialized it shows
five values.

**SQL statement for initializing the history table :**

.. code-block:: python

   query = """INSERT INTO history (date, place, fact)
                        VALUES
                        ('6th century AD', 'India', 'Game generated'),
                        ('15th century', 'Europe', 'Move of pieces changed'),
                        ('19th century', '..' ,'Modern tournament play began'),
                        ('1883', '..' , 'Chess clock first used'),
                        ('1886', '..', 'First world chess championship')"""
            cursor.execute(query)

Add fact
++++++++
The user can add new fact in the table by clicking *add fact* button. All information should be entered exxcept the place,
which is optional since that attribute can be NULL.

**SQL statement for adding a fact :**

.. code-block:: python

   def addfact(self, date, place, fact):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO history (date, place, fact)
                        VALUES
                        ('%s', '%s', '%s')""" % (date, place, fact)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('history'))


Find fact
+++++++++

You can find a fact from the table by either its number or by entering its date and/or place.

**SQL statement for finding a fact by its number :**

.. code-block:: python

   def findfact(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM history WHERE number = %s """ % (number)
            cursor.execute(query)
            history = cursor.fetchall()
        return render_template('findfact.html', history = history)

**SQL statement for finding a fact by place and/or date :**

.. code-block:: python

   def find_fact(self, date, place):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM history
                        WHERE date LIKE '%s%%'
                          AND place LIKE '%s%%'
                        ORDER BY number """ % (date, place)
            cursor.execute(query)
            history = cursor.fetchall()
        return render_template('findfact.html', history = history)

Delete fact
+++++++++++
Same options that are used for finding a fact are used also for deleting it.

**SQL statement for deleting a fact by its number :**

.. code-block:: python

   def deletefact(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM history WHERE number = '%s' """ % (number)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('history'))

**SQL statement for deleting a fact by place and/or date :**

.. code-block:: python

   def delete_fact(self, date, place):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM history WHERE date = '%s'
                        AND place = '%s' """ % (date, place)
            cursor.execute(query)
            connection.commit()
        return redirect(url_for('history'))


Update fact
+++++++++++
The user can update a fact by clicking the date of the fact that wants to update. The update fact page willopen.
Since the table does not have any foreign key, any information can be changed.

**SQL statement for opening update fact page :**

.. code-block:: python

   def open_updatefact(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM history WHERE number  = %s" % (number)
            cursor.execute(query)
            fact_up = cursor.fetchone()
        return render_template('updatefact.html', fact_up = fact_up)


**SQL statement for updating a fact :**

.. code-block:: python

   def fact_update(self, number, date, place, fact):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE history
                        SET date = '%s', place = '%s',
                            fact = '%s'
                        WHERE number = %s""" % (date, place, fact, number)
            cursor.execute(query)
        return redirect(url_for('history'))