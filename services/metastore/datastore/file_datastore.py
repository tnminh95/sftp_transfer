from services.metastore.datastore.datastore import DataStore
import json
import os
class FileDataStore(DataStore):
    def __init__(self, *args, **kwargs):
        self.file_path = kwargs["file_path"]

    def initialize(self):
        pass

    def save(self, input):
        json_object = json.dumps(input, indent=4)
        # Writing to sample.json
        with open(self.file_path, "w") as outfile:
            outfile.write(json_object)
    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    print("JSON data loaded successfully:")
                    print(data)
                    return data
                except json.JSONDecodeError as e:
                    print(f"Failed to decode JSON: {e}")
                    return []

        else:
            return []
