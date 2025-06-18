from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["animal_shelter"]
collection = db["aac_outcomes"]

# CREATE
def create_animal(data):
    if isinstance(data, dict):
        result = collection.insert_one(data)
        return str(result.inserted_id)
    else:
        raise ValueError("Data must be a dictionary.")

# READ
def read_animals(query=None):
    if query is None:
        query = {}
    return list(collection.find(query))

# UPDATE
def update_animal(animal_id, update_data):
    if not isinstance(update_data, dict):
        raise ValueError("Update data must be a dictionary.")
    result = collection.update_one({"_id": ObjectId(animal_id)}, {"$set": update_data})
    return result.modified_count

# DELETE
def delete_animal(animal_id):
    result = collection.delete_one({"_id": ObjectId(animal_id)})
    return result.deleted_count
