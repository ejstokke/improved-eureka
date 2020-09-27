from flask import request, abort
from server.study_data import Study, University
from server.models import Review
from server import app 

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
    query = request.args.get("study")
    if query:
        try:
            return study.get_study_data_json(query)
        except:
            abort(404, description="Resource not found")

    return all_studies
