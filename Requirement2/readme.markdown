SOFTWARE ENGINEER PYTHON TEST
=============================

SCENARIO

Here at Opayo we are always looking at ways to improve our core automation tools and reporting dashboard’s. We love to test and simulate as much as we can.
Given a Relational Database Schema or NoSQL collection consisting of -
```
Table Name - transaction
Id string – primary key (please think about the randomness of this)
Date int – timestamp of payment in unix ms
Currency string – the currency type used i.e. £
Amount float - amount of the transaction i.e. 133.7
Vendor string – the vendor name for the transaction
CardType string/ENUM – the payment type i.e. Visa, Mastercard
CardNumber string – the card number of the requestor
Address string – the address of the requestor
CountryOrigin string – the country of transaction origin in CountryCode ie UK, US
```
Requirement 2

Author a script or startup code that will randomly generate and populate ~20000
transactions into a mysql/mongodb database. This script or startup code should use
a yaml configuration file to point to the mysql/mongodb database hostip:port and
provide auth creds to the database. The script should take a command line
argument of how many transactions it should generate.


Assumptions
-----------
1) Id column would be populated as UUID
2) Date is a reserved word so the column would be called TransactionDate
3) I assume the MySQL database should be installed separately and the access to the instance would be configured manually


Installation
------------

You can unzip the source from the zip file and then install all dependencies:

    cd test/Requirement2
    pip install -r requirements.txt

After you have done that, please open config.yml in the same folder and manually amend the database access:
```yaml
mysql:
    host: your_host
    user: your_user
    password: your_password
    db: your_database
    port: your_port
```
Execution
---------

To run the script open a terminal and execute the following command in the folder Requirement1 where opayo_test was installed:

```
python3 generate.py 10
```

You should see the confirmation that the script successfully completed its task:

```
10 transactions inserted
```

If no parameter provided, the script will insert 20000 randomly generated transactions 

Exceptions
----------
If you try to provide the number greater than 20000, the script throws the following error:

```
Sorry the volume of transactions is too big
```

