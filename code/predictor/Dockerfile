# Set the base image.
FROM python:3.8-slim

# Install required libraries.
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential git libpq-dev
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
