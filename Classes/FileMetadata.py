import time

class FileMetadata:
    def __init__(self, file_type, name, size, fingerprint, modified, updated = time.time()):
        self.file_type = file_type
        self.name = name
        self.size = size
        self.fingerprint = fingerprint
        self.modified = modified
        self.updated = updated
    
    def update(self, size, fingerprint):
        self.size = size
        self.fingerprint = fingerprint
        # self.modified = time.time()