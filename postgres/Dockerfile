FROM postgres:14.1

# Copying all SQL scripts for setting up the data (including schemes and tables)
COPY sql /docker-entrypoint-initdb.d

# Copying the data individually to ensure that data is inserted AFTER any database schema and table creation
# Note: the filenames are being decremented from 99
COPY data/submissions_sample.sql /docker-entrypoint-initdb.d/99-submissions_sample.sql
COPY data/comments_sample.sql /docker-entrypoint-initdb.d/98-comments_sample.sql


ENV POSTGRES_PASSWORD admin_password