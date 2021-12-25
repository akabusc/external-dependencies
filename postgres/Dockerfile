FROM postgres:14.1

COPY sql /docker-entrypoint-initdb.d
COPY data /docker-entrypoint-initdb.d
ENV POSTGRES_PASSWORD admin_password