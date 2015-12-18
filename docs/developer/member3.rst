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

