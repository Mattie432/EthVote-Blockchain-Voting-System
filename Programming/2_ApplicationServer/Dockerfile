##################################################
# 
# Dockerfile to build the Application Server
# Based on: Python 3.4
# 
##################################################

# Set the base image to Python 3.4
FROM python:3.5

# Do not buffer the output from stdout.
ENV PYTHONUNBUFFERED 1

# Set the working directory.
WORKDIR /usr/src/applicationserver/

# Copy our python webapp over.
COPY . /usr/src/applicationserver/

# Install our dependencies
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        libpq-dev \
        libffi-dev \
        libyaml-dev

# Install our webapp via pip
RUN pip3 install .

# Expose our ports
EXPOSE 80 5436

# Run django migrate command to setup database migration, then start the server.
#CMD . ./bin/docker_entrypoint
ENTRYPOINT [ "./bin/docker_entrypoint" ]
