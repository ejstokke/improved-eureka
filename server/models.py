from server import db

class Review(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    uni_code = db.Column(db.String(7), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return str({
            "user_id": self.user_id,
            "uni_code": self.uni_code,
            "rating": self.rating
        })