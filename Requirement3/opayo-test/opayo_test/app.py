import json
import sys
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
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def lambda_handler(event, context):
    logger.info(event)
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    
    select_statement = 'select * from transactions where TransactionDate > %(days)s '
    cardtype_statement = ' and CardType = %(card_type)s'
    country_statement = ' and CountryOrigin = %(country)s'
    amount_statement = ' and Amount between %(from)s and %(to)s'

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
