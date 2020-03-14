# Set the base image.
FROM postgres:11.4-alpine

# Configure environment variables.
ENV POSTGRES_DB="velocity"
ENV POSTGRES_PASSWORD="velocity"
ENV POSTGRES_USER="velocity"
COPY schema.sql /docker-entrypoint-initdb.d/
