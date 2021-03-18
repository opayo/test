import json
import os
import logging
import pymysql
import boto3
import rds_config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


#rds settings
host  = os.environ['DB_HOST']
port = os.environ['DB_PORT']
db_name = os.environ['DB_NAME']
password = rds_config.DB_PASSWORD
user = rds_config.DB_USER

try:
    conn = pymysql.connect(host=host, user=user, passwd=password, port=int(port),
                            db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    raise e

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def lambda_handler(event, context):
    params = event['queryStringParameters']
    select_statement = 'select * from transactions where TransactionDate > UNIX_TIMESTAMP(DATE_ADD(CURDATE(),INTERVAL - %(days)s DAY)) '
    if 'n' not in params:
        raise Exception('Please provide the n parameter for the last n days')
    bind_variables = {"days": params['n']}
    
    if 'CardType' in params:
        select_statement += ' and CardType = %(card_type)s'
        bind_variables['card_type'] = params['CardType']
    
    if 'CountryOrigin' in params:
        select_statement += ' and CountryOrigin = %(country)s'
        bind_variables['country'] = params['CountryOrigin']
        
    if 'AmountFrom' in params and 'AmountTo' in params:
        select_statement += ' and Amount between %(from)s and %(to)s'
        bind_variables['from'] = params['AmountFrom']
        bind_variables['to'] = params['AmountTo']
    
    result = None
    try:
        with conn.cursor() as cur:
            cur.execute(select_statement, bind_variables)
            result = cur.fetchall()
    except:
         logger.error({"ERROR": "Unexpected error: Could not query MySQL instance.", "statement":select_statement, "bind_variables":bind_variables, "event":event})
         raise
    
    return {
        "statusCode": 200,
        "body": json.dumps({"result":result}),
    }
