# Set the base image.
FROM gcc:8

# Install required libraries.
RUN apt update && apt install -y cmake libpqxx-dev

# Install dockerize.
ENV DOCKERIZE_VERSION v0.6.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Copy the source files.
RUN mkdir /apps
WORKDIR /apps
COPY . /apps/

# Compile the application.
RUN cmake .
RUN make -j1

# Start the webserver
CMD dockerize -wait "tcp://database:5432" -timeout 1m ./server "postgres://velocity:velocity@database:5432/velocity" 8080
