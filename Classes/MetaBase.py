import time 
from database import delete_one

class MetaBase:
    def __init__(self):
        self.metadata_by_name_and_type = {}
        self.metadata_by_type = {}
        self.metadata_in_db = {}

    def check_key(self, file_type, name):
        key = (name, file_type)
        if key in self.metadata_by_name_and_type or key in self.metadata_in_db:
            return False
        return True

    def insert(self, metadata):
        key = (metadata.name, metadata.file_type)
        if key in self.metadata_by_name_and_type or key in self.metadata_in_db:
            return False
        self.metadata_by_name_and_type[key] = metadata
        if metadata.file_type not in self.metadata_by_type:
            self.metadata_by_type[metadata.file_type] = []
        self.metadata_by_type[metadata.file_type].append(metadata)
        return True

    def get(self, file_type, name):
        key = (name, file_type)
        return self.metadata_by_name_and_type.get(key, None)
    
    def get_from_db(self, file_type, name):
        key = (name, file_type)
        return self.metadata_in_db.get(key, None)

    def get_all_by_type(self, file_type):
        return self.metadata_by_type.get(file_type, [])

    def delete(self, file_type, name):
        key = (name, file_type)
        metadata = self.metadata_by_name_and_type.get(key, None)
        if metadata:
            del self.metadata_by_name_and_type[key]
            self.metadata_by_type[file_type].remove(metadata)
            return True
        elif self.metadata_in_db.get(key, None):
            metadata = self.metadata_in_db.get(key, None)
            delete_one(metadata)

            del self.metadata_in_db[key]
            self.metadata_by_type[file_type].remove(metadata)
            return True
        return False

    def delete_all(self):
        self.metadata_by_name_and_type.clear()
        self.metadata_by_type.clear()

    def compare(self, metadata):
        existing_metadata = self.get(metadata.file_type, metadata.name)
        existing_metadata_in_db = self.get_from_db(metadata.file_type, metadata.name)

        if existing_metadata:
            if existing_metadata.fingerprint == metadata.fingerprint and existing_metadata.size == metadata.size and existing_metadata.modified == metadata.modified:
                existing_metadata.updated = time.time()
                return "Success"
            elif existing_metadata.modified == metadata.modified and existing_metadata.size == metadata.size and existing_metadata.fingerprint != metadata.fingerprint:
                return "Warning"
            elif existing_metadata.fingerprint == metadata.fingerprint and existing_metadata.modified != metadata.modified and existing_metadata.size != metadata.size:
                return "Failed"
        elif existing_metadata_in_db:
            if existing_metadata_in_db.fingerprint == metadata.fingerprint and existing_metadata_in_db.size == metadata.size and existing_metadata_in_db.modified == metadata.modified:
                existing_metadata_in_db.updated = time.time()
                return "Success"
            elif existing_metadata_in_db.modified == metadata.modified and existing_metadata_in_db.size == metadata.size and existing_metadata_in_db.fingerprint != metadata.fingerprint:
                return "Warning"
            elif existing_metadata_in_db.fingerprint == metadata.fingerprint and existing_metadata_in_db.modified != metadata.modified and existing_metadata_in_db.size != metadata.size:
                return "Failed"

        return "Not Found"