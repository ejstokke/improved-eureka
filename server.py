from flask import Flask, request
from StudyData import Study, University

app = Flask(__name__)

uni = University()
all_unis = uni.get_all_universities_json()
study = Study()
all_studies = study.get_all_studies_json()

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
        return study.get_study_data_json(query)

    return all_studies

if __name__ == '__main__':
    app.run(debug=True)