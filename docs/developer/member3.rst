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

Initializing the table
++++++++++++++++++++++
The upcoming events table can be initialized by pressing the *initialize table* button that is above the table.
When the table is initialized it shows eight events.

**SQL statement for initializing the upcoming events table : **

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

**SQL statement for aadding an event to the table : **

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

SQL statement for finding event by the number on the table :

.. code-block:: python

   def find_event(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM events WHERE number = %s """ % (number)
            cursor.execute(query)
            events = cursor.fetchall()
            cursor.close()
        return render_template('findevent.html', events = events)

SQL statement for finding event by date and place :

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

SQL statement for finding event by championship :

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

SQL statement for deleting an event by the number on the table :

.. code-block:: python

   def deleteevent(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM events WHERE number = '%s' """ % (number)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('upcoming_events'))



SQL statement for deleting an event by the date and place :

.. code-block:: python

   def delete_event(self, date, place):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM events WHERE date = '%s'
                        AND place = '%s' """ % (date, place)
            cursor.execute(query)

SQL statement for deleting an event by the championship :

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

SQL statement for opening the  update event page :

.. code-block:: python

   def open_updatetour(self, number):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM tours WHERE number  = %s" % (number)
            cursor.execute(query)
            tour_up = cursor.fetchone()
        return render_template('updatetour.html', tour_up = tour_up)


SQL statement for updating an event :

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
