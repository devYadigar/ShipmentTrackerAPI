CREATE DATABASE IF NOT EXISTS shipment_db;
CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON shipment_db.* TO 'user'@'%';
GRANT ALL PRIVILEGES ON test_shipment_db.* TO 'user'@'%';
FLUSH PRIVILEGES;