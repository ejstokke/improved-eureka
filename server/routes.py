from flask import request, abort
from server.models import Review, University, Study
from server.verification import review_exists
from server import app, db

# uni = University()
# all_unis = uni.get_all_universities_json()
# study = Study()
# all_studies = study.get_all_studies_json()


@app.route('/universities')
def universities():
    query = request.args.get("university")
    if query:
        uni_data = University.query.filter_by(uni_code=query.upper()).first()
        if not uni_data: 
            abort(404, description="Resource not found")
        return str(uni_data)

    return str(University.query.all())


@app.route('/studies')
def studies():
    study_query = request.args.get("study_code")
    uni_query = request.args.get("university")

    if study_query:
        result = Study.query.filter_by(study_code=study_query.upper()).all()
        if not result:
            abort(404, description="Resource not found")
        return str(result)

    if uni_query:
        result = Study.query.filter_by(uni_code=uni_query.upper()).all()
        if not result:
            abort(404, description="Resource not found")
        return str(result)
            

    return str(Study.query.all())


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
        uni_query = request.args.get("uni_code")

        if user_query and uni_query:
            review = Review.query.filter_by(user_id=user_query, uni_code=uni_query).first()
            return str(review)

        if user_query:
            review = Review.query.filter_by(user_id=user_query).all()
            return str(review)

        if uni_query:
            review = Review.query.filter_by(uni_code=uni_query.upper()).all()
            return str(review)

        reviews = Review.query.all()
        return str(reviews)
