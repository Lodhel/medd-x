import pymongo


class BaseMongo:
    def connect(self):
        conn = pymongo.MongoClient('localhost', 27017)

        db = conn['knowledge_base']

        coll = db["health"]

        doc = {"name": "Иван", "surname": "Иванов"}
        coll.save(doc)

