from server.models import Review
from server import db

def review_exists(user_id, uni_code):
    review = Review.query.filter_by(user_id=user_id, uni_code=uni_code).first()
    if review:
        return True
    return False