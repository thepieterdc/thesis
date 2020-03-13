# Set the base image.
FROM alpine

# Install required libraries.
RUN apk add --update build-base cmake libarchive-dev pugixml-dev sqlite-dev

# Copy the source files.
RUN mkdir /apps
WORKDIR /apps
COPY . /apps/

# Compile the application.
RUN cmake .
RUN make -j2 web

# Start the webserver
CMD ./web /data/database.db 8080
