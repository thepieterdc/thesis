# Set the base image.
FROM gcc:8

# Install required libraries.
RUN apt update && apt install -y cmake libarchive-dev libpugixml-dev libpqxx-dev

# Copy the source files.
RUN mkdir /apps
WORKDIR /apps
COPY . /apps/

# Compile the application.
RUN cmake .
RUN make -j2 server

# Start the webserver
CMD ["./server",  "postgres://velocity:velocity@database:5432/velocity", "8080"]
