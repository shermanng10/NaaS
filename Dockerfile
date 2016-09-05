FROM ubuntu:14.04

RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev
RUN apt-get -yqq install postgresql postgresql-contrib libpq-dev

ADD . /opt/app
WORKDIR /opt/app

RUN pip install -r requirements.txt
