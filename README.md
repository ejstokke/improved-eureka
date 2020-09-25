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

--------

### Studies
#### GET
Returns application data about a study which includes: university, grade points needed, extra requirements needed.
* `/studies` for every study course

* `/studies?study=184395` to get particular study with code 184395

--------

### Universities
#### GET
Returns object with amount of students at a university.

* `/universities`

* `/universities?university=UIB` to get data about UIB
