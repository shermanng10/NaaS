# NaaS (Niceness as a Service)
[![Build Status](https://travis-ci.org/shermanng10/NaaS.svg?branch=master)](https://travis-ci.org/shermanng10/NaaS)

An API built with Flask/Psycopg2/Docker that returns random compliments as well as accepts user submitted compliments.

# How to set it up:
- Install Docker
- Clone repo and navigate to root directory.
- Run:
```
docker-compose build
docker-compose up
docker exec naas_api_1 flask initdb
```
- Navigate to localhost:5000 in your browser.
