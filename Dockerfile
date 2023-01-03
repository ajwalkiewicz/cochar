# apline 3.17 and python 3.8
# copied from https://github.com/docker-library/python/blob/f5b7b5a332bd4d2c1518325ab9647b09bf07412f/3.8/alpine3.17/Dockerfile

FROM ubuntu:20.04

# set the working directory
WORKDIR /cochar

RUN apt-get update
RUN apt-get upgrade --yes
RUN apt-get install python3.8 python3-pip --yes

# install dependencies
COPY ./dev_requirements.txt .

RUN pip install --no-cache-dir --upgrade -r dev_requirements.txt

# copy the scripts to the folder
COPY . /cochar

RUN pip install -e .
