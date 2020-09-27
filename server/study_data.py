import json
import sys
import pandas as pd
from time import time
from uni_codes import uni_codes

FILE_NAME_STUDY = "\\uhg-poenggrenser-hovedopptaket-2020.xlsx"
FILE_NAME_UNI = "\\lærested_for_studenter.csv"
FILE_LOCATION_STUDY = sys.path[0] + FILE_NAME_STUDY
FILE_LOCATION_UNI = sys.path[0] + FILE_NAME_UNI

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


    def get_study_data_json(self, study_code):
        '''
        Creates a JSON object for a study

        Arguments:
            study_code {string} -- [Studiekode fra samordna opptak]

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
        

    def get_all_studies_json(self):
        all_studies = list()

        for study_code in self.df["Studiekode"]:
            all_studies.append(self.get_study_data_json(study_code))

        return json.dumps(all_studies)


class University:

    UNI_CODES = uni_codes

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


    def get_uni_data_json(self, uni_code):
        '''
        Returns a json object with amount of male and female students for a university

        Arguments:
            uni_code {string} [Feks UIB, NHH or OSLOMET as in Study]

        Returns:
            [String] -- [JSON]
        '''
        uni_data = {
            "Sted": None,
            "Begge kjønn": None,
            "Menn": None,
            "Kvinner": None
        }

        if self.__uni_code_is_valid(uni_code):
            row = self.__find_row(uni_code)
            for col in row:
                uni_data[col] = str(row.iloc[0][col])

            json_data = json.dumps(uni_data)
            return json_data
        return False


    def get_all_universities_json(self):
        all_universities = list()

        for kode in University.UNI_CODES:
            all_universities.append(self.get_uni_data_json(kode))

        return json.dumps(all_universities)        


if __name__ == "__main__":
    start = time()

    study = Study()
    uni = University()

    print(uni)
    print(study)

    x = study.get_study_data_json("191345")
    y = uni.get_uni_data_json("HVO")
    # print(x)
    # print(y)

    #all_uni = uni.get_all_universities_json()
    #all_studies = study.get_all_studies_json()
    # print(all_uni)
    #print(len(all_studies))
    

    end = time()
    print(f"Finished in {(end - start):.3f} seconds")
    
    