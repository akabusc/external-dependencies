#!/bin/bash

# We do this in a shell script running 'psql' so we can connect to the database after creating it.
psql -p 5432 -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
-- Create the database user
CREATE USER dbadmin WITH PASSWORD 'admin_password';
CREATE USER training_admin WITH PASSWORD 'admin_password';

-- Create the database
CREATE DATABASE training WITH OWNER=training_admin
                                  LC_COLLATE='en_US.utf8'
                                  LC_CTYPE='en_US.utf8'
                                  ENCODING='UTF8'
                                  TEMPLATE=template0;

EOSQL
