# API for MyUNI app
## Installation
Windows:
* Install [python 3.7](https://www.python.org/downloads/release/python-372/)
* `pip install pipenv`
* `pipenv install`

## Running the server
Use the following commands to run server on localhost:5000
* `pipenv shell`
* `pipenv run start`

## Endpoints
### Studies
#### GET
Returns application data about a study which includes: university, grade points needed, extra requirements needed.
* `/studies` for every study course

* `/studies?study=STUDIEKODE` where STUDIEKODE is e.g. 184453 for information science

--------

### Universities
#### GET
Returns object with amount of students at a university.

* `/universities`

* `/universities?university=UNIVERSITYCODE` where UNIVERSITYCODE is e.g. UIB for University of bergen
