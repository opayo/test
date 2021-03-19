import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

import mysql.connector

mydb = mysql.connector.connect(
  host=cfg["mysql"]["host"],
  user=cfg["mysql"]["user"],
  password=cfg["mysql"]["password"],
  port=cfg["mysql"]["port"],
  database=cfg["mysql"]["db"],
  autocommit=True
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS transactions (id VARCHAR(255)  NOT NULL PRIMARY KEY, TransactionDate INT, Currency VARCHAR(3), Amount FLOAT, Vendor VARCHAR(255), CardType ENUM('Visa','Mastercard', 'AMEX'), CardNumber VARCHAR(16), Address VARCHAR(255), CountryOrigin VARCHAR(2))")

import random
import uuid 
import time
import string

currencies = ('GH₵', 'ብር', '₹', '₹', '£', '₹', '₹', 'ريال', 'лв.', 'K', 'DA', 'DH', '₹', '₹', 'रु', 'VT', '৳', '₹', '¥', '₹', '$', '₽', 'NT$', '₴', 'zł', 'CHF', '₹', 'ރ.', '¤', '₪', '₦', '€', '֏', '₪')
countries = ('AF','AX','AL','DZ','AS','AD','AO','AI','AQ','AG','AR','AM','AW','AU','AT','AZ','BS','BH','BD','BB','BY','BE','BZ','BJ','BM','BT','BO','BQ','BA','BW','BV','BR','IO','BN','BG','BF','BI','CV','KH','CM','CA','KY','CF','TD','CL','CN','CX','CC','CO','KM','CD','CG','CK','CR','CI','HR','CU','CW','CY','CZ','DK','DJ','DM','DO','EC','EG','SV','GQ','ER','EE','SZ','ET','FK','FO','FJ','FI','FR','GF','PF','TF','GA','GM','GE','DE','GH','GI','GR','GL','GD','GP','GU','GT','GG','GN','GW','GY','HT','HM','VA','HN','HK','HU','IS','IN','ID','IR','IQ','IE','IM','IL','IT','JM','JP','JE','JO','KZ','KE','KI','KP','KR','KW','KG','LA','LV','LB','LS','LR','LY','LI','LT','LU','MO','MK','MG','MW','MY','MV','ML','MT','MH','MQ','MR','MU','YT','MX','FM','MD','MC','MN','ME','MS','MA','MZ','MM','NA','NR','NP','NL','NC','NZ','NI','NE','NG','NU','NF','MP','NO','OM','PK','PW','PS','PA','PG','PY','PE','PH','PN','PL','PT','PR','QA','RE','RO','RU','RW','BL','SH','KN','LC','MF','PM','VC','WS','SM','ST','SA','SN','RS','SC','SL','SG','SX','SK','SI','SB','SO','ZA','GS','SS','ES','LK','SD','SR','SJ','SE','CH','SY','TW','TJ','TZ','TH','TL','TG','TK','TO','TT','TN','TR','TM','TC','TV','UG','UA','AE','GB','UM','US','UY','UZ','VU','VE','VN','VG','VI','WF','EH','YE','ZM','ZW')

card_type = ('Visa','Mastercard','AMEX')

add_transaction = "INSERT INTO transactions (id, TransactionDate, Currency, Amount, Vendor, CardType, CardNumber, address, CountryOrigin) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

import sys

try:
    n = int(sys.argv[1])
except IndexError as error:
    n = 20000
    
if n > 20000:
    raise Exception('Sorry the volume of transactions is too big')

for i in range(n):
    transaction_data = (
        str(uuid.uuid1()),
        time.time() - random.randint(0, 10 * 365 * 24 * 60 * 60),
        currencies[random.randint(0, len(currencies) - 1)],
        random.randint(1, 100000) / 100,
        "".join(
            random.choice(string.ascii_lowercase) for i in range(random.randint(9, 19))
        ),
        card_type[random.randint(0, len(card_type) - 1)],
        random.randint(1000000000000000, 9999999999999999),
        " ".join(
            "".join(
                random.choice(string.ascii_lowercase)
                for i in range(random.randint(9, 15))
            )
            for j in range(random.randint(5, 15))
        ),
        countries[random.randint(0, len(countries) - 1)]
    )

    mycursor.execute(add_transaction, transaction_data)

print(n, 'transactions  inserted')

mycursor.close
mydb.close
