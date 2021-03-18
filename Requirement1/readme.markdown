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
Requirement 1

Write a REST service with the Python framework of your choice connecting to a
mysql/mongodb database. We should be able to query this service to obtain the
following information -
1. Transactions made in the last n days, where n is provided by the requestor.
2. The number of transactions made in the last n days where CardType is xyz ,
where n and xyz are provided by the requestor.
3. A list of all the transactions made in the last n days where the CountryOrigin
is xyz , where n and xyz are provided by the requestor.
4. A list of all transactions made in the last n days where the Amount is between
abc and xyz , where n , abc and xyz are provided by the requestor.

Assumptions
-----------
1) The output format has not been specified in the technical test so I assumed I could return the transactions as the array:
```
[['0491d83e-87d4-11eb-ad7d-068cf7dea69a', 1616037000, '£', 267.11, 'Tesco', 'Visa', '2247561869095639', 'London', 'UK'],
['04b5c140-87d4-11eb-ad7d-068cf7dea69a', 1615806369, '$', 746.96, 'Wallmart', 'Visa', '3203116777107131', 'New York', 'US'],
['04cb34da-87d4-11eb-ad7d-068cf7dea69a', 1615829018, '¥', 439.5, 'Ma-suya Azabu-Juban', 'AMEX', '7456389190278573', 'Tokio', 'JP']
...........
]
```
2) I assume the MySQL database should be installed separately and the access to the instance would be added manually


Installation
------------

You can unzip the source from zip file and then install all dependancies:

    unzip opayo_test.zip
    cd test/Requirement1
    pip install -r requirements.txt

After you have done that, please open rds_config.py in the same folder and manually amend the database access:
```python
DB_HOST = 'your_host'
DB_PORT = your_port
DB_USER = 'your_user'
DB_PASSWORD = 'your_password'
DB_NAME = 'your_database'
```
Execution
---------

To run the server locally execute the following command in the folder Requirement1 where opayo_test was installed:

```
python3 api.py 
```

You should immediately see the confirmation that the server is up and running:

```
* Serving Flask app "api" (lazy loading)
 * Environment: production
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
```

Tests
---------

To run the unit tests open the same folder Requirement1 in another terminal window and execute the following:

```
python3 -m unittest discover -v
```

You should get the following response

```
test_amount (test_api.TestTransactions) ... ok
test_card_type (test_api.TestTransactions) ... ok
test_country_origin (test_api.TestTransactions) ... ok
test_days (test_api.TestTransactions) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.862s

OK
```

Transactions API
---------
The API supports the GET method and returns the transactions matching the criteria provided by the requestor.

To obtain the list of transactions made in the last n days, you should send the request with `n` as a key e.g. `{n:5}` to the end point `http://localhost:5000/transactions`

The response you receive would be in the list format:
```
[['0491d83e-87d4-11eb-ad7d-068cf7dea69a', 1616037000, '£', 267.11, 'febbkitabczwcfw', 'Visa', '2247561869095639', 'owcjaiypqdkm hauuvhvtrw lqygwiwhpgb zskbferojlgpa xzbfamscnh nacjnywuwd lkmjduatcefdhrf pjlvrmyrf jnnppdlxavlbs eflcwganfdm glmxcbyprpld niijvexghrdikw igguehady', 'AD'],..........]
```

If you were constructing the URL by hand, this data would be given as key/value pairs in the URL after a question mark, e.g. `http://localhost:5000/transactions?n=3`

Or you can use any available third party frameworks to access the Transactions API but the following example is written in Python using [Requests]( https://requests.readthedocs.io/en/master/):

```python
import requests   
 
url = 'http://localhost:5000/transactions'
input_params = {"n":3}

response = requests.get(url, params= input_params )

print(response.text)

#[[['0491d83e-87d4-11eb-ad7d-068cf7dea69a', 1616037000, '£', 267.11, 'Tesco', 'Visa', '2247561869095639', 'London', 'UK'], ['04b5c140-87d4-11eb-ad7d-068cf7dea69a', 1615806369, '$', 746.96, 'Wallmart', 'Visa', '3203116777107131', 'New York', 'US'], ['04cb34da-87d4-11eb-ad7d-068cf7dea69a', 1615829018, '¥', 439.5, 'Ma-suya Azabu-Juban', 'AMEX', '7456389190278573', 'Tokio', 'JP']..........

```
While n is a mandatory parameter, Transactions API supports optional parameters:
CardType to filter out the transactions by card type
CountryOrigin to filter out them by country
and a pair of parameters AmountFrom and AmountTo to obtain the list of all transactions where the Amount is between AmountFrom and AmountTo 

Fill in the transactions 
----------
If you want to fill the database instance with randomly generated data, please see the readme file in Requirement2


Exceptions
----------
If you try to access the API without the parameter `n` in the requests, you will receive the following error:

```
Argument "n" is not found
```

