from server import db

class Review(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    uni_code = db.Column(db.String(7), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Review({self.user_id}, {self.uni_code}, {self.rating})"