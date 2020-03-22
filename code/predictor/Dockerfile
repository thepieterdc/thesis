# Set the base image.
FROM python:3.6-alpine

# Install required libraries.
RUN apk add --update build-base git postgresql-dev
RUN pip3 install gitpython numpy psycopg2

# Copy the source files.
RUN mkdir /app
WORKDIR /app
COPY . /app/

# Copy the initialisation scripts.
COPY docker-entrypoint-cli.sh /usr/bin/entrypoint-cli.sh
RUN chmod +x /usr/bin/entrypoint-cli.sh

COPY docker-entrypoint-daemon.sh /usr/bin/entrypoint-daemon.sh
RUN chmod +x /usr/bin/entrypoint-daemon.sh
