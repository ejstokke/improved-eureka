from flask import request, abort
from server.study_data import Study, University
from server.models import Review
from server.verification import review_exists
from server import app, db

uni = University()
all_unis = uni.get_all_universities_json()
study = Study()
all_studies = study.get_all_studies_json()


@app.route('/universities')
def universities():
    query = request.args.get("university")
    if query:
        uni_data = uni.get_uni_data_json(query) 
        if not uni_data: 
            abort(404, description="Resource not found")
        return uni_data

    return all_unis


@app.route('/studies')
def studies():
    query = request.args.get("study") # Her trengs mer query-alternativer for filtrering / søk
    if query:
        try:
            return study.get_study_data_json(query) 
        except:
            abort(404, description="Resource not found")

    return all_studies


@app.route('/universities/reviews', methods=["GET", "POST"])
def reviews():
    if request.method == "POST":
        data = request.json

        if review_exists(data["user_id"], data["uni_code"]):
            abort(403, description="Review already exists") # Replace this code with deleting existing entry and storing new one

        review = Review(user_id=data["user_id"], uni_code=data["uni_code"], rating=data["rating"])
        db.session.add(review)
        db.session.commit()
        return f"Posted {review}"
    
    if request.method == "GET":
        user_query = request.args.get("user_id")
        uni_query = request.args.get("uni_code").upper()

        if user_query and uni_query:
            review = Review.query.filter_by(user_id=user_query, uni_code=uni_query).first()
            return str(review)

        if user_query:
            review = Review.query.filter_by(user_id=user_query).all()
            return str(review)

        if uni_query:
            review = Review.query.filter_by(uni_code=uni_query).all()
            return str(review)

        reviews = Review.query.all()
        return str(reviews)
