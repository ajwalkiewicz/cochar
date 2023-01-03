FROM python:3.8-alpine

RUN apk add --no-cache --virtual .build-deps build-base linux-headers pcre-dev

# set the working directory
WORKDIR /webapp

# install dependencies
COPY ./dev_requirements.txt .
RUN pip install --no-cache-dir --upgrade -r dev_requirements.txt

# clean .build-deps
# RUN apk del --no-network .build-deps

# copy the scripts to the folder
COPY . /webapp

# start the server
CMD ["uwsgi", "--http", "0.0.0.0:80", "--master", "-p", "4", "-w", "wsgi", "--py-autoreload", "3"]
# CMD ["python3", "webapp.py"]
