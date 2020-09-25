# API for MyUNI app
## Installation
Windows:
* Install [python 3.7](https://www.python.org/downloads/release/python-372/)
* `pip install pipenv`
* `pipenv install`

## Running the server
Use the following commands to run server on localhost:5000
* `pipenv shell`
* `python server.py`

## Endpoints
Run server.py which will start a server on localhost:5000

--------

* `/studies` for every study course

* `/studies?study=184395` to get particular study with code 184395

--------

* `/universities`

* `/universities?university=UIB` to get data about UIB
