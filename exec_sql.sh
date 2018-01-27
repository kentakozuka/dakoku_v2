#/bin/bash

mysql -h db -P 3306 -u root -p < create_tables.sql > /dev/null
