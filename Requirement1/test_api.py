import unittest
import rds_config
import pymysql
import requests

import random
import uuid 
import time
import string

currencies = ('GH₵', 'ብር', '₹', '₹', '£', '₹', '₹', 'ريال', 'лв.', 'K', 'DA', 'DH', '₹', '₹', 'रु', 'VT', '৳', '₹', '¥', '₹', '$', '₽', 'NT$', '₴', 'zł', 'CHF', '₹', 'ރ.', '¤', '₪', '₦', '€', '֏', '₪')
countries = ('AF','AX','AL','DZ','AS','AD','AO','AI','AQ','AG','AR','AM','AW','AU','AT','AZ','BS','BH','BD','BB','BY','BE','BZ','BJ','BM','BT','BO','BQ','BA','BW','BV','BR','IO','BN','BG','BF','BI','CV','KH','CM','CA','KY','CF','TD','CL','CN','CX','CC','CO','KM','CD','CG','CK','CR','CI','HR','CU','CW','CY','CZ','DK','DJ','DM','DO','EC','EG','SV','GQ','ER','EE','SZ','ET','FK','FO','FJ','FI','FR','GF','PF','TF','GA','GM','GE','DE','GH','GI','GR','GL','GD','GP','GU','GT','GG','GN','GW','GY','HT','HM','VA','HN','HK','HU','IS','IN','ID','IR','IQ','IE','IM','IL','IT','JM','JP','JE','JO','KZ','KE','KI','KP','KR','KW','KG','LA','LV','LB','LS','LR','LY','LI','LT','LU','MO','MK','MG','MW','MY','MV','ML','MT','MH','MQ','MR','MU','YT','MX','FM','MD','MC','MN','ME','MS','MA','MZ','MM','NA','NR','NP','NL','NC','NZ','NI','NE','NG','NU','NF','MP','NO','OM','PK','PW','PS','PA','PG','PY','PE','PH','PN','PL','PT','PR','QA','RE','RO','RU','RW','BL','SH','KN','LC','MF','PM','VC','WS','SM','ST','SA','SN','RS','SC','SL','SG','SX','SK','SI','SB','SO','ZA','GS','SS','ES','LK','SD','SR','SJ','SE','CH','SY','TW','TJ','TZ','TH','TL','TG','TK','TO','TT','TN','TR','TM','TC','TV','UG','UA','AE','GB','UM','US','UY','UZ','VU','VE','VN','VG','VI','WF','EH','YE','ZM','ZW')

card_type = ('Visa','Mastercard','AMEX')

class TestTransactions(unittest.TestCase):

    url = 'http://localhost:5000/transactions'
    
    conn = pymysql.connect(host=rds_config.DB_HOST, user=rds_config.DB_USER, passwd=rds_config.DB_PASSWORD, port=rds_config.DB_PORT,
                                    db=rds_config.DB_NAME, connect_timeout=5, autocommit=True)
                                    
    def __init__(self, *args, **kwargs): 
        super(TestTransactions, self).__init__(*args, **kwargs)
        
        create_table = "CREATE TABLE IF NOT EXISTS transactions (id VARCHAR(255)  NOT NULL PRIMARY KEY, TransactionDate INT, Currency VARCHAR(3), Amount FLOAT, Vendor VARCHAR(255), CardType ENUM('Visa','Mastercard', 'AMEX'), CardNumber VARCHAR(16), Address VARCHAR(255), CountryOrigin VARCHAR(2))"
        
        with self.conn.cursor() as cur:
            response = cur.execute(create_table)

                                    
    def insert_transaction(self, days, CardType = None, CountryOrigin = None, AmountFrom = None, AmountTo = None):
        add_transaction = "INSERT INTO transactions (id, TransactionDate, Currency, Amount, Vendor, CardType, CardNumber, address, CountryOrigin) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        transaction_data = (
            str(uuid.uuid1()),
            time.time() - random.randint(0, days * 24 * 60 * 60),
            currencies[random.randint(0, len(currencies) - 1)],
            random.randint(1 if AmountFrom is None else AmountFrom*100, 100000 if AmountTo is None else AmountTo*100) / 100,
            "".join(
                random.choice(string.ascii_lowercase) for i in range(random.randint(9, 19))
            ),
            CardType if CardType is not None else card_type[random.randint(0, len(card_type) - 1)],
            random.randint(1000000000000000, 9999999999999999),
            " ".join(
                "".join(
                    random.choice(string.ascii_lowercase)
                    for i in range(random.randint(9, 15))
                )
                for j in range(random.randint(5, 15))
            ),
            CountryOrigin if CountryOrigin is not None else countries[random.randint(0, len(countries) - 1)]
        )
    
        with self.conn.cursor() as cur:
            response = cur.execute(add_transaction, transaction_data)
        
        return transaction_data
        
    def test_days(self):
        days = random.randint(365, 365*10)
        data = self.insert_transaction(days)
        response = requests.get(self.url, params={"n":days})

        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.headers["Content-Type"] == "application/json")
        self.assertTrue(next(item for item in response.json()["result"] if item[0] == data[0]))

    def test_country_origin(self):
        days = random.randint(365, 365*10)
        CountryOrigin = countries[random.randint(0, len(countries) - 1)]
        data = self.insert_transaction(days, CountryOrigin = CountryOrigin)
        response = requests.get(self.url, params={"n":days, "CountryOrigin":CountryOrigin})
        
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.headers["Content-Type"] == "application/json")
        self.assertTrue(next(item for item in response.json()["result"] if item[0] == data[0] and data[8] == CountryOrigin))

    def test_card_type(self):
        days = random.randint(365, 365*10)
        CardType = card_type[random.randint(0, len(card_type) - 1)]
        data = self.insert_transaction(days, CardType = CardType)
        response = requests.get(self.url, params={"n":days, "CardType":CardType})
        
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.headers["Content-Type"] == "application/json")
        self.assertTrue(next(item for item in response.json()["result"] if item[0] == data[0] and data[5] == CardType))

    def test_amount(self):
        days = random.randint(365, 365*10)
        AmountFrom = random.randint(99,100000)/100
        AmountTo = random.randint(AmountFrom*100, 100000)
        data = self.insert_transaction(days, AmountFrom = AmountFrom, AmountTo = AmountTo)
        response = requests.get(self.url, params={"n":days, "AmountFrom":AmountFrom, "AmountTo":AmountTo})
        
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.headers["Content-Type"] == "application/json")
        self.assertTrue(next(item for item in response.json()["result"] if item[0] == data[0] and data[3] >= AmountFrom and data[3] <= AmountTo))

if __name__ == '__main__':
    unittest.main()