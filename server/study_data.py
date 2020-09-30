import json
import sys
import pandas as pd
from time import time
from uni_codes import uni_codes, valid_uni_codes
from server import db
from server.models import University as UniModel
from server.models import Study as StudyModel

# Might want to change this to use os.environ instead
FILE_NAME_STUDY = "\\uhg-poenggrenser-hovedopptaket-2020.xlsx"
FILE_NAME_UNI = "\\lærested_for_studenter.csv"
FILE_LOCATION_STUDY = sys.path[0] + FILE_NAME_STUDY
FILE_LOCATION_UNI = sys.path[0] + FILE_NAME_UNI

# This is just a script to process data from Samordna Opptak and insert into DB

class Study: 

    def __init__(self, file_location=FILE_LOCATION_STUDY):
        self.df = pd.read_excel(file_location, skiprows=18, mangle_dupe_cols=True)


    def __repr__(self):
        return f"Study(file_location='{FILE_LOCATION_STUDY}')"


    def __get_grade_points(self, row):
        ord_grade, ordf_grade = row["Poenggrense"], row["Poenggrense.1"]
        return ord_grade, ordf_grade
    

    def __find_row(self, study_code):
        row = self.df.query(f'Studiekode == {study_code}')
        return row.iloc[0]


    def get_study_data(self, study_code):
        '''
        Creates a dict for a study program

        Arguments:
            study_code {string} -- [Studiekode fra samordna opptak]

        Returns:
            [Dict]

        '''
        row = self.__find_row(study_code)
        ordi, ordf = self.__get_grade_points(row)
        study_data = {
            "Studiekode": str(row["Studiekode"]),
            "Studienavn": row["Studienavn"],
            "Lærestedskode": row["Lærestedskode"],
            "Utdanningsområde": row["Utdanningsområde og type"],
            "Ordinær": ordi,
            "Førstegang": ordf,
        }

        return study_data
        

    def get_all_studies(self):
        all_studies = list()

        for study_code in self.df["Studiekode"]:
            all_studies.append(self.get_study_data(study_code))

        return all_studies


class University:

    UNI_CODES = valid_uni_codes
    ALL_UNI_CODES = uni_codes

    def __init__(self, file_location=FILE_LOCATION_UNI):
        df = pd.read_csv(file_location, sep=";", skiprows=2)
        self.df = df.drop(labels="Unnamed: 4", axis="columns")


    def __repr__(self):
        return f"University(file_location='{FILE_LOCATION_UNI}')"


    def __find_row(self, uni_code):
        uni_name = University.UNI_CODES[uni_code]
        row = self.df.loc[self.df["Sted"] == uni_name]
        return row
        

    def __uni_code_is_valid(self, uni_code):
        if uni_code in University.UNI_CODES:
            return True

        return False


    def get_uni_data(self, uni_code, to_json=False):
        '''
        Returns an object with amount of male and female students for a university

        Arguments:
            uni_code {string} [Feks UIB, NHH or OSLOMET as in Study]
            json {Boolean} [Whether you want python dict or JSON]

        Returns:
            [Dict] -- [Data about all universities]
        '''
        uni_data = {
            "Uni_code": uni_code,
            "Sted": None,
            "Begge kjønn": None,
            "Menn": None,
            "Kvinner": None
        }

        if self.__uni_code_is_valid(uni_code):
            row = self.__find_row(uni_code)
            for col in row:
                uni_data[col] = str(row.iloc[0][col])

            if to_json:    
                json_data = json.dumps(uni_data)
                return json_data
            
            return uni_data

        else:
            uni_data["Sted"] = University.ALL_UNI_CODES[uni_code]
            
            if to_json:
                json_data = json.dumps(uni_data)
                return json_data
            
            return uni_data

        return False


    def get_all_universities_json(self):
        all_universities = list()

        for kode in University.UNI_CODES:
            all_universities.append(self.get_uni_data(kode))

        return json.dumps(all_universities)        


def populate_database(create_table=False, wipe_data=False):
    
    if create_table:
        db.create_all()
    if wipe_data:
        StudyModel.query.delete()
        UniModel.query.delete()
    uni = University()
    study = Study()

    for uni_code in uni_codes:
        data = uni.get_uni_data(uni_code)
        uni_row = UniModel(uni_code=data["Uni_code"], name=data["Sted"], total_students=data["Begge kjønn"], male_students=data["Menn"], female_students=data["Kvinner"])
        db.session.add(uni_row)
        db.session.commit()

    # all_studies = study.get_all_studies()
    # for study_data in all_studies:
    #     study_row = StudyModel(
    #         study_code=study_data["Studiekode"],
    #         programme_name=study_data["Studienavn"],
    #         uni_code=study_data["Lærestedskode"],
    #         education_field=study_data["Utdanningsområde"],
    #         ordinary=study_data["Ordinær"],
    #         ordinary_first=study_data["Førstegang"]
    #     )
    #     db.session.add(study_row)
    #     db.session.commit()


# populate_database(create_table=True)
# print(StudyModel.query.all())
# print(UniModel.query.all())