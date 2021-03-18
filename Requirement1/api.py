import logging
import flask
import json
from flask import request, make_response
from datetime import datetime


import rds_config;
import pymysql;


logger = logging.getLogger()
logger.setLevel(logging.INFO)

#rds settings
host  = rds_config.DB_HOST
port = rds_config.DB_PORT
db_name = rds_config.DB_NAME
password = rds_config.DB_PASSWORD
user = rds_config.DB_USER



conn = pymysql.connect(host=host, user=user, passwd=password, port=int(port),
                            db=db_name, connect_timeout=5, autocommit=True)


app = flask.Flask(__name__)
app.config["DEBUG"] = True

headers = {"Content-Type": "application/json"}

def execute_select(days, CardType , CountryOrigin , AmountFrom , AmountTo ):
    select_statement = 'select * from transactions where TransactionDate > UNIX_TIMESTAMP(DATE_ADD(CURDATE(),INTERVAL - %(days)s DAY)) '
    bind_variables = {"days":days}

    if CardType is not None:
        select_statement += ' and CardType = %(card_type)s'
        bind_variables["card_type"] = CardType

    if CountryOrigin is not None:
        select_statement += ' and CountryOrigin = %(country)s'
        bind_variables["country"] = CountryOrigin
        
    if AmountFrom is not None and AmountTo is not None:
        select_statement += ' and Amount between %(from)s and %(to)s'
        bind_variables["from"] = AmountFrom
        bind_variables["to"] = AmountTo
        
    with conn.cursor() as cur:
        cur.execute(select_statement, bind_variables)
        result = cur.fetchall()
     
    return result

@app.route('/transactions', methods=['GET'])
def home():
    #first try to get the numbers from the args property
    days = request.args.get("n", type=int)
    card_type = request.args.get("CardType")
    country = request.args.get("CountryOrigin")
    amount_from = request.args.get("AmountFrom", type=float)
    amount_to = request.args.get("AmountTo", type=float)
    
    if days is None:
        raise Exception('Argument "n" is not found')
            
    result = execute_select(days, card_type, country, amount_from, amount_to)

    return make_response({"result":result}, 200)

if __name__ == '__main__':
    app.run()
