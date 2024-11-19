1: Create the database.
sql

CREATE DATABASE transaction_db;
2: Use the created database.

sql

USE transaction_db;


3. Create the transactions table  columns.

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_date DATETIME,
    CardType VARCHAR(50),
    CountryOrigin VARCHAR(50),
    Amount DECIMAL(10, 2)
);


4.  insert some sample data into the table for testing purposes:
INSERT INTO transactions (transaction_date, CardType, CountryOrigin, Amount)
VALUES 
    ('2023-06-01 10:00:00', 'Visa', 'USA', 120.00),
    ('2023-06-02 12:00:00', 'Mastercard', 'Germany', 330.00),
    ('2023-06-03 14:00:00', 'Amex', 'UK', 520.00);

5. run You can run this script from the command line by specifying the number of transactions to generate as an argument.  to generate 20,000 transactions:

python task2_transactions 20000