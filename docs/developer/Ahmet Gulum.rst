Parts Implemented by Ahmet Gülüm
================================
Benefit table
-------------
This table shows benefits of the chess game.In the database the table is named as "benefit".
The table has three columns;id,benefit and type.But in the website id column is not showed.
The primary key of the table is the id of the benefit and it is generated serially.
The benefits are unique in this table beceuse the benefit column is  foreign key of other table.

+------------+--------+----------+-------------+-----------+--------+
| Attribuite | Type   | Not Null | Primary key | Reference | Unique |
+============+========+==========+=============+===========+========+
| id         | serial | 1        | Yes         | No        | Yes    |
+------------+--------+----------+-------------+-----------+--------+
| Benef      | text   | 1        | No          | No        | Yes    |
+------------+--------+----------+-------------+-----------+--------+
| Type       | text   | 1        | No          | No        | No     |
+------------+--------+----------+-------------+-----------+--------+

   - *id* is the primary key
   - *Benef* is the name of benefit
   - *Type* is the type of benefit

 **SQL statement for creating the benefit table : **

.. code-block:: python

     query = """CREATE TABLE IF NOT EXISTS benefit (
                        ID serial PRIMARY KEY,
                        Benef text UNIQUE NOT NULL,
                        Type text NOT NULL)"""
            cursor.execute(query)

Initializing the Table
++++++++++++++++++++++
The Benefit Table can be initialized by pressing the *Initialize Table* button that is below of the page.
When the table is initialized it shows 7 benefits.

  **SQL statement for initializing Benefit Table **

.. code-block:: python

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
Adding Benefit
++++++++++++++
Benefits can be added to the benefit table by filling the fields below the benefit table and clicking 'Add Benefit'.
User should give values for Benefit and Type attributes.
While adding a new benefit,the user should take into consideration that the new benefit can not have the same name with any other
benefit in the table since the benefit attribute is unique.

  **SQL statement for adding a benefit to the table : **

.. code-block:: python

   def addbenefit(self, Benef,Type):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO benefit (Benef,Type)
                        VALUES
                        ('%s', '%s')""" % (Benef,Type)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('benefit_page'))

Find Benefit
++++++++++++
Benefits can be retrieved from the benefit table in two ways. One of them is to find a benefit by its name
and the other method is by its type.
There are two buttons.First one is for finding by name and it has a label "Find Benefit".
Second one is for finding by type and it has a label "Find Benefit By Type".

  **SQL statement for finding benefit by name : **

.. code-block:: python

      query = """SELECT Benef, Type FROM benefit
                        WHERE Benef = '%s'""" % (Benef)

            cursor.execute(query)

**SQL statement for finding benefit by type : **

.. code-block:: python

      query = """SELECT Benef, Type FROM benefit
                        WHERE Type = '%s'""" % (Type)

            cursor.execute(query)

Delete Benefit
++++++++++++++
Benefits can be deleted from the benefit table byits name.
To delete a benefit,the user should enter name of the benefit and push *Delete Benefit* button.
If the benefit is used in the other tables,delete operation will be done for all of them.

  **SQL statement for deleting a benefit : **

.. code-block:: python

      query = """DELETE FROM benefit WHERE Benef = '%s' """ % (Benef)
            cursor.execute(query)

Update Benefit
++++++++++++++
Benefits can be updated by suppling name of the benefit that is wanted to update,new name of that benefit and
new type of that benefit.
If this benefit is used in the other tables, update operation will be cascaded.

  **SQL statement for updating a benefit : **

.. code-block:: python

      query = """UPDATE benefit
                        SET Benef= '%s',
                            Type = '%s'
                             WHERE Benef = '%s' """ % (new,new2,Benef)
            cursor.execute(query)

People table
------------
This table shows people and their benefit.In the database the table is named as "people".
The table has three columns;Peopleid,Name and HasBenefit.But in the website Peopleid column is not showed.
The primary key of the table is the Peopleid of the benefit and it is generated serially.
The names are unique in this table beceuse name column is  foreign key of other table.

+------------+--------+----------+-------------+-----------+--------+
| Attribuite | Type   | Not Null | Primary key | Reference | Unique |
+============+========+==========+=============+===========+========+
| Peopleid   | serial | 1        | Yes         | No        | Yes    |
+------------+--------+----------+-------------+-----------+--------+
| Name       | text   | 1        | No          | No        | Yes    |
+------------+--------+----------+-------------+-----------+--------+
| HasBenefit | text   | 1        | No          | Yes       | No     |
+------------+--------+----------+-------------+-----------+--------+

   - *Peopleid* is the primary key
   - *Name* is the name of the people
   - *HasBenefit* is the name benefit that people have

 **SQL statement for creating people table : **

.. code-block:: python

     query = """CREATE TABLE IF NOT EXISTS people (
                        Peopleid serial PRIMARY KEY,
                        Name text UNIQUE NOT NULL,
                        HasBenefit text  NOT NULL references benefit(Benef)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE)"""
            cursor.execute(query)

Initializing the Table
++++++++++++++++++++++
People Table can be initialized by pressing the *Initialize Table2* button that is below of the page.
When the table is initialized it shows 7 people.

  **SQL statement for initializing people Table **

.. code-block:: python

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

Adding People
+++++++++++++
A peoson can be added to people table by filling the fields name,benefit and clicking 'Add People'.
While adding a new people,the user should take into consideration that new people can not have the same name with any other
people in the table since the benefit attribute is unique.
Also entered benefit should be present in the benefit table.

  **SQL statement for adding a people : **

.. code-block:: python

   def addpeople(self, Name,HasBenefit):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO people (Name,HasBenefit)
                        VALUES
                        ('%s', '%s')""" % (Name,HasBenefit)
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('benefit_page'))

Find People
+++++++++++
The people can be retrieved from  people table in two ways. One of them is to find people by its name
and the other method is by its benefit.
There are two buttons.First one is for finding by name and it has a label "Find People".
Second one is for finding by type and it has a label "Find People By Benefit".

  **SQL statement for finding benefit by name : **

.. code-block:: python

      query = """SELECT Benef, Type FROM benefit
                        WHERE Benef = '%s'""" % (Benef)

            cursor.execute(query)

**SQL statement for finding benefit by type : **

.. code-block:: python

      query = """SELECT Benef, Type FROM benefit
                        WHERE Type = '%s'""" % (Type)

            cursor.execute(query)

Delete People
+++++++++++++
People can be deleted from the people table by its name.
To delete a person,the user should enter name of the person and push *Delete People* button.
If the person is used in the other tables,delete operation will be done for all of them.

  **SQL statement for deleting a person : **

.. code-block:: python

      query = """DELETE FROM people WHERE Name = '%s' """ % (Name)
            cursor.execute(query)

Update People
+++++++++++++
People can be updated by suppling name of the person that is wanted to update,new name of that person and
new benefit of that person.
If this person is used in the other tables, update operation will be done for all of them.

  **SQL statement for updating a benefit : **

.. code-block:: python

      query = """UPDATE people
                        SET Name= '%s',
                            HasBenefit='%s'
                             WHERE Name = '%s' """ % (new,new2,Name)
            cursor.execute(query)

Relation table
--------------
This table shows relationship between people and benefit with duration.In the database the table is named as "relation".
The table has four columns;id,ThePeople, TheBenefit and duration.But in the website id column is not showed.
The primary key of the table is the id that is generated serially.
ThePeople and TheBenefit are unique in this table beceuse they are  foreign keys of other tables.

+------------+--------+----------+-------------+-----------+--------+
| Attribuite | Type   | Not Null | Primary key | Reference | Unique |
+============+========+==========+=============+===========+========+
| id         | serial | 1        | Yes         | No        | Yes    |
+------------+--------+----------+-------------+-----------+--------+
| ThePeople  | text   | 1        | No          | No        | Yes    |
+------------+--------+----------+-------------+-----------+--------+
| TheBenefit | text   | 1        | No          | Yes       | No     |
+------------+--------+----------+-------------+-----------+--------+
| duration   | text   | 1        | No          | Yes       | No     |
+------------+--------+----------+-------------+-----------+--------+


   - *Peopleid* is the primary key
   - *ThePeople* is the name of the person
   - *TheBenefit* is the name of the benefit that people have
   - *Tduration* is the duration of the benefit that people have

 **SQL statement for creating relation table : **

.. code-block:: python

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

Initializing the Table
++++++++++++++++++++++
Relation Table can be initialized by pressing the *Initialize Table3* button that is below of the page.
When the table is initialized it shows 7 relation.

  **SQL statement for initializing relation Table **

.. code-block:: python

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

Adding People
+++++++++++++
A relation can be added to relation table by filling the fields name,benefit,duration and clicking 'Add Relation'.
While adding a new relation,the user should take into consideration that benefit and people in new relation
must exist in benefit and people table.


  **SQL statement for adding a relation : **

.. code-block:: python

   query = """INSERT INTO relation (ThePeople,TheBenefit,duration)
                        VALUES
                        ('%s', '%s','%s')""" % (ThePeople,TheBenefit,duration)
            cursor.execute(query)

Find Relation
+++++++++++++
The relation can be retrieved from  relation table by the name of person.

  **SQL statement for finding relation : **

.. code-block:: python

        query = """SELECT ThePeople,TheBenefit,duration FROM relation
                        WHERE ThePeople = '%s'""" % (ThePeople)

            cursor.execute(query)


Delete Relation
+++++++++++++++
A relation can be deleted from the relaiton table by the name of the person.
To delete a relation,after entering the name of the person, the user should push *Delete People* button.


  **SQL statement for deleting a relation : **

.. code-block:: python

      query = """DELETE FROM relation WHERE ThePeople = '%s' """ % (ThePeople)
            cursor.execute(query)

Update Relation
+++++++++++++++
A relation can be updated by suppling name of the person in the relation,new name of that person,
new benefit of that person and new duration of this relation.
While aupdating a relation,the user should take into consideration that benefit and people in new relation
must exist in benefit and people table

  **SQL statement for updating a relation : **

.. code-block:: python

       query = """UPDATE relation
                        SET TheBenefit= '%s',
                            duration= '%s',
                            ThePeople='%s'
                             WHERE ThePeople = '%s' """ % (new,new2,new3,ThePeople)
            cursor.execute(query)







