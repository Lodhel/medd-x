import pymongo


class BaseMongo:
    def connect(self):
        conn = pymongo.MongoClient('localhost', 27017)

        db = conn['knowledge_base']

        return db["health"]

    def create_default_data(self):

        data = {
            "Condition or Disease": [
                "Excludes the presence of condition",
                "Confirms the presence of condition",
                "Supposes the presence of condition",
                "Indicates low intensity of condition",
                "Indicates middle intensity of condition",
                "Indicates high intensity of condition",
                "Impact not define"
            ],
            "Symptom": [
                "Excludes the presence of condition",
                "Confirms the presence of condition",
                "Supposes the presence of condition",
                "Indicates low intensity of condition",
                "Indicates middle intensity of condition",
                "Indicates high intensity of condition",
                "Impact not define"
            ],
            "Human parameter": [],
            "Lifestyle and habits": [],
            "Diet and nutrition": [],
            "Environment Influence": [],
            "Anamnesis and Chronic": [],
            "Procedure or Exam": [],
            "Genetic heredity": [],
            "Laboratory test": [],
            "Treatment": [],
            "Allergy or Asthma": [],
            "Additional information": [],
            "Cause of pathology": []
        }
        coll = self.connect()
        coll.save(data)

    def get(self, key):
        coll = self.connect()
        data = [info for info in coll.find(key)]

        return {key: data}

    def all_destroy(self):
        coll = self.connect()
        coll.remove({})


