import json
import sys
import pandas as pd
from timeit import timeit

FILE_NAME_STUDY = "\\uhg-poenggrenser-hovedopptaket-2020.xlsx"
FILE_NAME_UNI = "\\lærested_for_studenter.csv"
FILE_LOCATION_STUDY = sys.path[0] + FILE_NAME_STUDY
FILE_LOCATION_UNI = sys.path[0] + FILE_NAME_UNI

class Study: 

    def __init__(self, file_location=FILE_LOCATION_STUDY):
        self.df = pd.read_excel(file_location, skiprows=18, mangle_dupe_cols=True)


    def __get_grade_points(self, row):
        ord_grade, ordf_grade = row["Poenggrense"], row["Poenggrense.1"]
        return ord_grade, ordf_grade
    

    def __find_row(self, study_code):
        row = self.df.query(f'Studiekode == {study_code}')
        return row.iloc[0]


    def get_json(self, study_code):
        '''
        Creates a JSON object for a study

        Arguments:
            study_code {string} -- [Studiekode]

        Returns:
            [String] -- [JSON]

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
        json_data = json.dumps(study_data)

        return json_data
        

class University:

    UNI_CODES = {
        "NHH": "Norges Handelshøyskole"
    }

    def __init__(self, file_location=FILE_LOCATION_UNI):
        df = pd.read_csv(file_location, sep=";", skiprows=2)
        self.df = df.drop(labels="Unnamed: 4", axis="columns")

    def __find_row(self, uni_code):
        '''
        Arguments:
            uni_code {string} [Feks UIB, NHH or OSLOMET as in Study]
        '''
        uni_name = University.UNI_CODES[uni_code]
        row = self.df.loc[self.df["Sted"] == uni_name]
        return row
        

    def __uni_code_is_valid(self, uni_code):
        if uni_code in University.UNI_CODES:
            return True

        return False


    def get_json(self, uni_code):
        uni_data = {
            "Sted": "",
            "Begge Kjønn": "",
            "Menn": "",
            "Kvinner": ""
        }

        if self.__uni_code_is_valid(uni_code):
            row = self.__find_row(uni_code)
            for col in row:
                uni_data[col] = str(row.iloc[0][col])

        json_data = json.dumps(uni_data)
        return json_data


if __name__ == "__main__":
    start = timeit()

    study = Study()
    uni = University()
    x = study.get_json("191345")
    y = uni.get_json("NHH")
    print(x)
    print(y)

    end = timeit()
    print(f"Finished in {(end - start):.3f} seconds")
    
    