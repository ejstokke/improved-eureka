from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from study_data import Study, University


DEBUG_MODE = True
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Review(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    uni_code = db.Column(db.String(7), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Review({self.user_id}, {self.uni_code}, {self.rating})"


# db.drop_all() # Drops all tables and rows
# db.create_all() # To create all tables


@app.route('/universities')
def universities():
    query = request.args.get("university")
    if query:
        return uni.get_uni_data_json(query)

    return all_unis


@app.route('/studies')
def studies():

    query = request.args.get("study")
    if query:
        try:
            return study.get_study_data_json(query)
        except:
            return f"<h1>404</h1> Found no study with code {query}</p>"

    return all_studies


if __name__ == '__main__':
    uni = University()
    all_unis = uni.get_all_universities_json()
    study = Study()
    all_studies = study.get_all_studies_json()

    app.run(debug=DEBUG_MODE)