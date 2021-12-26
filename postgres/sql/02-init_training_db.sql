\connect training

-- create roles, initial users, and schema
CREATE ROLE training_read_only;
CREATE ROLE training_user;

GRANT training_read_only TO training_user;
GRANT training_user TO training_admin;
GRANT training_admin TO dbadmin;

-- create a user for connecting to the db manually
CREATE
    USER training_script_user PASSWORD 'user_password' IN ROLE training_user;

-- reduced-privilege app user (DML operations only)
CREATE
    USER training_app PASSWORD 'app_password' IN ROLE training_user;

-- enable login to training_admin role so we can use it for database migrations
-- only way to ensure objects created in migration scripts are owned by training_admin
ALTER
    ROLE training_admin LOGIN PASSWORD 'admin_password';

-- data is intended to be populated with sample data by this repo
CREATE SCHEMA data AUTHORIZATION training_admin;

-- search is intended to be created by the application service
CREATE SCHEMA search AUTHORIZATION training_admin;

-- set current and database default search path to include both search and data schema
SET
    search_path = search,data,public;
ALTER
    DATABASE training SET search_path = search,data,public;

GRANT USAGE ON SCHEMA
    search TO training_read_only;
GRANT CREATE
    ON SCHEMA search TO training_admin;

-- setup default privileges for training_admin users
ALTER
    DEFAULT PRIVILEGES FOR ROLE training_admin IN SCHEMA search GRANT
    SELECT
    ON TABLES TO training_read_only;

ALTER
    DEFAULT PRIVILEGES FOR ROLE training_admin IN SCHEMA search GRANT INSERT,
    UPDATE,
    DELETE
    ON TABLES TO training_user;

ALTER
    DEFAULT PRIVILEGES FOR ROLE training_admin IN SCHEMA search GRANT
    SELECT
    ON SEQUENCES TO training_read_only;

ALTER
    DEFAULT PRIVILEGES FOR ROLE training_admin IN SCHEMA search GRANT USAGE ON SEQUENCES TO training_user;

ALTER
    DEFAULT PRIVILEGES FOR ROLE training_admin IN SCHEMA search GRANT EXECUTE ON FUNCTIONS TO training_user;

-- enable trigram indexing
CREATE
    EXTENSION pg_trgm SCHEMA public;

-- enable case-insensitive text field
CREATE
    EXTENSION citext SCHEMA public;