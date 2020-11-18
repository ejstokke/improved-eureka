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


class University(db.Model):
    uni_code = db.Column(db.String(7), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_students = db.Column(db.Integer)
    male_students = db.Column(db.Integer)
    female_students = db.Column(db.Integer)
    studies = db.relationship('Study', lazy=True, backref="university")

    def __repr__(self):
        return str({
            "uni_code": self.uni_code,
            "name": self.name,
            "total students": self.total_students,
            "male students": self.male_students,
            "female students": self.female_students
        })


class Study(db.Model):
    study_code = db.Column(db.Integer, primary_key=True)
    programme_name = db.Column(db.String(200), nullable=False)
    uni_code = db.Column(db.String(10), db.ForeignKey('university.uni_code'))
    education_field = db.Column(db.String(25))
    ordinary = db.Column(db.String(4))
    ordinary_first = db.Column(db.String(4))

    def __repr__(self):
        return str({
            "study_code": self.study_code,
            "programme_name": self.programme_name,
            "uni_code": self.uni_code,
            "education_field": self.education_field,
            "ordinary": self.ordinary,
            "ordinary_first": self.ordinary_first
        })

    def return_object(self):
        return {
            "study_code": self.study_code,
            "programme_name": self.programme_name,
            "uni_code": self.uni_code,
            "education_field": self.education_field,
            "ordinary": self.ordinary,
            "ordinary_first": self.ordinary_first
        }