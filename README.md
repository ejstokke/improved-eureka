# API for MyUNI app
## Installation
Windows:
* Install [python 3.8](https://www.python.org/downloads/release/python-382/)
* `pip install pipenv`
* `pipenv install`

## Running the server
Use the following commands to run the server:
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

* `/universities?university=UNIVERSITYCODE` where UNIVERSITYCODE is e.g. UIB for University of Bergen

--------

### Reviews
A review is an object consisting of a user id, the code for the university they reviewed, and a rating number.
#### GET
* `/user/reviews` to get all reviews

* `/user/reviews?user_id=INT&uni_code=UNIVERSITYCODE` to get a specific review

* `/user/reviews?uni_code=UNIVERSITYCODE` to get all reviews for a university.

* `/user/reviews?user_id=INT` to get all reviews for a user

#### POST
* `/user/reviews` Post a review object.

* `{
  user_id: 1,
  uni_code: "UIB",
  rating: 5
}`
