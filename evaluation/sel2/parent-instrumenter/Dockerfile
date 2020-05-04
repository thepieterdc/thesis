FROM alpine

RUN apk add git

# Clone the repository.
RUN git clone https://5ef1cefe8569ddf4a7ebbba3d0956fbde3098e6b:x-oauth-basic@github.ugent.be/piedcler/2017-2018-groep-05.git /app

# Checkout the commit.
WORKDIR /app

# Copy the workflow and instrumenter.
COPY instrumenter.sh /instrumenter.sh
COPY runner.sh /runner.sh
COPY workflow.yml /workflow.yml
RUN chmod +x /instrumenter.sh