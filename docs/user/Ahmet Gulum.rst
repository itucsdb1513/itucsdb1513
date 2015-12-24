Parts Implemented by Ahmet Gülüm
================================

To access Benefits page from home page of *Chess*, click *Benefits* bar as shown below picture.

.. figure:: gulum_picture/main.png
      :scale: 50 %
      :alt: Main

      *This is the main page*

Benefits Page
+++++++++++++

.. figure:: gulum_picture/benefits.png
      :scale: 50 %
      :alt: Main

      *This is the benefits page*


Benefit Table

.. figure:: gulum_picture/benefittable.png
      :scale: 50 %
      :alt: Main


+-----------+--------+---------------------+-+
| Attribute | Type   | Explanation         | |
+===========+========+=====================+=+
| id        | serial | ID of the benefits  | |
+-----------+--------+---------------------+-+
| Benefit   | string | Name of the Benefit | |
+-----------+--------+---------------------+-+
| Type      | string | Type of the Benefit | |
+-----------+--------+---------------------+-+


In this table there are 2 columns displayed to the user. Id column is not displayed.

There are five operations that can be carried on the table. Those are:
  - Add Benefit
  - Find Benefit
  - Find Benefit by Type
  - Delete Benefit
  - Update Benefit

Add Benefit
-----------

If the user wants to add a benefit to the table the user should fill the fields shown below and click on the button "Add Benefit".

.. figure:: gulum_picture/addbenefit.png
      :scale: 50 %
      :alt: Add Benefit to Benefits Table
|


After the user fills the fields and clicks on the "Add Benefit" the benefit is added to the table and displayed in it.

Delete Benefit
--------------
A benefit can be deleted from the table by name.
After entering the name to be deleted , "Delete Benefit" button is clicked.


.. figure:: gulum_picture/deletebenefit.png
      :scale: 50 %
      :alt: Delete Benefit
|

Find Benefit
------------

A benefit can be searched by typing name of it which the user wants to display.
After the name is typed into the field, the "Find Benefit" button should be clicked to perform the action.
Search results will be shown below of the benefits page under the search results 1.

.. figure:: gulum_picture/findbenefit.png
      :scale: 50 %
      :alt: Find Benefit by name
|


Result of the search operation.

.. figure:: gulum_picture/searchresult1.png
      :scale: 50 %
      :alt: Found Benefits is shown below of the page
|



Find Benefit by Type
--------------------
The benefit can be searched by typing type of it which the user wants to display.
After the type is entered into the field, the "Find Benefit by Type" button should be clicked to perform the action.
Search results will be shown below of the benefits page under the search results 1.

.. figure:: gulum_picture/findbenefitbytype.png
      :scale: 50 %
      :alt: Find Benefit by type
|


Result of the search operation.

.. figure:: gulum_picture/searchresult2.png
      :scale: 50 %
      :alt: Found Benefits is shown below of the page
|


Update Benefit
--------------

To update a benefit , the user should type new name and new type of benefit, then click "Update Benefit".

.. figure:: gulum_picture/updatebenefit.png
      :scale: 50 %
      :alt: updating benefit
|

People Table


.. figure:: gulum_picture/peopletable.png
      :scale: 50 %
      :alt: Main

+-----------+--------+-------------------------+-+
| Attribute | Type   | Explanation             | |
+===========+========+=========================+=+
| Peopleid  | serial | ID of people            | |
+-----------+--------+-------------------------+-+
| Name      | string | Name of person          | |
+-----------+--------+-------------------------+-+
| Benefit   | string | Benefit that person has | |
+-----------+--------+-------------------------+-+



In this table there are 2 columns displayed to the user. Peopleid column is not displayed.

There are five operations that can be carried on the table. Those are:
  - Add People
  - Find People
  - Find People by Benefit
  - Delete People
  - Update People

Add People
----------

If the user wants to add a person to the table, the user should fill the fields shown below and click on the button "Add People".

.. figure:: gulum_picture/addpeople.png
      :scale: 50 %
      :alt: Add People
|


After the user fills the fields and clicks on the "Add People" the person is added to the table and displayed in it.

Delete People
-------------
The person can be deleted from the table by name.
After entering the name to be deleted , "Delete People" button is clicked.


.. figure:: gulum_picture/deletepeople.png
      :scale: 50 %
      :alt: Delete People
|

Find People
-----------

The person can be searched by typing name of it which the user wants to display.
After the name is typed into the field, the "Find People" button should be clicked to perform the action.
Search results will be shown below of the benefits page under the search results 2.

.. figure:: gulum_picture/findpeople.png
      :scale: 50 %
      :alt: Find Benefit by name
|


Result of the search operation.

.. figure:: gulum_picture/searchresult3.png
      :scale: 50 %
      :alt: Found Benefits is shown below of the page
|



Find People by Benefit
----------------------
The person can be searched by typing Benefit that he has, which the user wants to display.
After the benefit is entered into the field, the "Find People by Benefit" button should be clicked to perform the action.
Search results will be shown below of the benefits page under the search results 2.

.. figure:: gulum_picture/findpeoplebybenefit.png
      :scale: 50 %
      :alt: Find people by benefit
|


Result of the search operation.

.. figure:: gulum_picture/searchresult4.png
      :scale: 50 %
      :alt: Found Benefits is shown below of the page
|


Update People
-------------

To update a person , the user should type name of the person, new name and new benefit, then click "Update People".

.. figure:: gulum_picture/updatepeople.png
      :scale: 50 %
      :alt: updating people
|

Relation Table

.. figure:: gulum_picture/relationtable.png
      :scale: 50 %
      :alt: Main

+-----------+--------+-------------------------+-+
| Attribute | Type   | Explanation             | |
+===========+========+=========================+=+
| id        | serial | ID of relation          | |
+-----------+--------+-------------------------+-+
| Name      | string | Name of person          | |
+-----------+--------+-------------------------+-+
| Benefit   | string | Benefit that person has | |
+-----------+--------+-------------------------+-+
| Duration  | string | Duration of Benefit     | |
+-----------+--------+-------------------------+-+




In this table there are 3 columns displayed to the user. Peopleid column is not displayed.

There are five operations that can be carried on the table. Those are:
  - Add Relation
  - Find Relation
  - Find Relation by duration
  - Delete Relation
  - Update Relation

Add Relation
------------

If the user wants to add a relation to the table, the user should fill the fields shown below and click on the button "Add Relation".

.. figure:: gulum_picture/addrelation.png
      :scale: 50 %
      :alt: Add Relation
|


After the user fills the fields and clicks on the "Add Relation" the relation is added to the table and displayed in it.

Delete Relation
---------------
The relation can be deleted from the table by name.
After entering the name to be deleted , "Delete Relation" button is clicked.


.. figure:: gulum_picture/deleterelation.png
      :scale: 50 %
      :alt: Delete Relation
|

Find Relation
-------------

The relation can be searched by typing name of it which the user wants to display.
After the name is typed into the field, the "Find Relation" button should be clicked to perform the action.
Search results will be shown below of the benefits page under the search results 3.

.. figure:: gulum_picture/findrelation.png
      :scale: 50 %
      :alt: Find Benefit by name
|


Result of the search operation.

.. figure:: gulum_picture/searchresult5.png
      :scale: 50 %
      :alt: Found Relations
|



Find Relation by Duration
-------------------------
The relation can be searched by typing duration, which the user wants to display.
After the duration is entered into the field, the "Find Relation by Duration" button should be clicked to perform the action.
Search results will be shown below of the benefits page under the search results 3.

.. figure:: gulum_picture/findrelationbyduration.png
      :scale: 50 %
      :alt: Find relation by duration
|


Result of the search operation.

.. figure:: gulum_picture/searchresult6.png
      :scale: 50 %
      :alt: Found Relations
|


Update Relation
---------------

To update a relation , the user should type name of the person, new name , new benefit and new duration, then click "Update Relation".

.. figure:: gulum_picture/updaterelation.png
      :scale: 50 %
      :alt: Update Relation
|




