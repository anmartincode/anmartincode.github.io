from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
import jsonschema

class AnimalShelter:
    # Define the JSON schema for animal data
    animal_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "number"},
            "animal_type": {"type": "string"},
            "breed": {"type": "string"},
            "outcome": {"type": "string"}
        },
        "required": ["name", "age", "animal_type", "breed", "outcome"]
    }

    def __init__(self, host, port, username, password):
        # Set up structured logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
        self.logger = logging.getLogger(__name__)
        try:
            self.client = MongoClient(
                host=host,
                port=int(port),
                username=username,
                password=password,
                authSource='admin'
            )
            self.db = self.client['AAC']
            self.logger.info("Connection to MongoDB successful!")
        except ConnectionFailure as e:
            self.logger.error(f"Could not connect to MongoDB: {e}")

    def create(self, data):
        # Validate data against schema
        try:
            jsonschema.validate(instance=data, schema=self.animal_schema)
        except jsonschema.ValidationError as ve:
            self.logger.error(f"Schema validation error: {ve.message}")
            raise Exception(f"Schema validation error: {ve.message}")
        if data is not None:
            insert_result = self.db.outcomes.insert_one(data)
            self.logger.info(f"Document inserted with ID: {insert_result.inserted_id}")
            return insert_result.acknowledged
        else:
            raise Exception("Nothing to save, data parameter is empty")

    def read(self, query):
        if query is not None:
            cursor = self.db.outcomes.find(query)
            result = [doc for doc in cursor]
            self.logger.info(f"Query returned {len(result)} documents.")
            return result
        else:
            raise Exception("Nothing to read, query parameter is empty")

    def update(self, query, update_data):
        if query is not None:
            update_result = self.db.outcomes.update_many(query, {"$set": update_data})
            self.logger.info(f"Updated {update_result.modified_count} documents.")
            return update_result.modified_count
        else:
            raise Exception("Nothing to update, query parameter is empty")

    def delete(self, query):
        if query is not None:
            delete_result = self.db.outcomes.delete_many(query)
            self.logger.info(f"Deleted {delete_result.deleted_count} documents.")
            return delete_result.deleted_count
        else:
            raise Exception("Nothing to delete, query parameter is empty")
