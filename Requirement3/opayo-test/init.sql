create database if not exists opayo;

CREATE TABLE IF NOT EXISTS opayo.transactions (id VARCHAR(255)  NOT NULL PRIMARY KEY, TransactionDate INT, Currency VARCHAR(3), Amount FLOAT, Vendor VARCHAR(255), CardType ENUM('Visa','Mastercard', 'AMEX'), CardNumber VARCHAR(16), Address VARCHAR(255), CountryOrigin VARCHAR(2));

CREATE USER "opayo-LambdaRole-1NWY78LZ9W0M" IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS'; 
            