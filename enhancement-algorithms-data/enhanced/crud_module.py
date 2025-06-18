from pymongo import MongoClient

class CRUD:
    def __init__(self, username, password, database, host='nv-desktop-services.apporto.com', port=32994):
        try:
            self.client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/?authSource=shelter_database")
            self.db = self.client[database]
            print("Connection to MongoDB successful!")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def create(self, collection, document):
        try:
            result = self.db[collection].insert_one(document)
            return result.acknowledged
        except Exception as e:
            print(f"Error: {e}")
            return False

    def read(self, collection, query):
        try:
            return list(self.db[collection].find(query))
        except Exception as e:
            print(f"Error: {e}")
            return []

    def update(self, collection, query, new_values):
        try:
            result = self.db[collection].update_one(query, {"$set": new_values})
            return result.modified_count
        except Exception as e:
            print(f"Error: {e}")
            return 0

    def delete(self, collection, query):
        try:
            result = self.db[collection].delete_one(query)
            return result.deleted_count
        except Exception as e:
            print(f"Error: {e}")
            return 0
