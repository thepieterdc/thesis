# Set the base image.
FROM python:3.7-alpine

# Install required libraries.
RUN apk add --update build-base git postgresql-dev
RUN pip3 install gitpython psycopg2

# Copy the source files.
RUN mkdir /app
WORKDIR /app
COPY . /app/

# Copy the initialisation script.
COPY docker-entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
