################################################################################
#### BUILD STAGE                                                               #
################################################################################

# Set the base image.
FROM alpine:latest AS builder

# Install packages.
RUN apk add build-base cmake pugixml-dev sqlite-dev

# Create a directory to store the files in.
RUN mkdir /build
WORKDIR /build

# Copy required files.
COPY . /build

# Build the application.
RUN cmake .
RUN make -j

################################################################################
#### EXECUTION STAGE                                                           #
################################################################################

# Set the base image.
FROM alpine:latest

# Install packages.
RUN apk add pugixml-dev sqlite-dev

# Copy the built application.
WORKDIR /root/
COPY --from=builder /build/analyser .
RUN chmod 0755 /root/analyser

# Start the application.
ENTRYPOINT /root/analyser
