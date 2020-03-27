FROM alpine

RUN apk add git

# Clone the repository.
RUN git clone https://6a031facfd18b1133f11084293f89124251804e7:x-oauth-basic@github.com/dodona-edu/dodona.git /app

# Checkout the commit.
WORKDIR /app

# Set the analysis remote.
RUN git remote add analysis https://6a031facfd18b1133f11084293f89124251804e7:x-oauth-basic@github.com/thepieterdc/dodona-analysis.git

# Copy the runner and instrumenter.
COPY instrumenter.sh /instrumenter.sh
COPY runner.sh /runner.sh
RUN chmod +x /instrumenter.sh
RUN chmod +x /runner.sh
