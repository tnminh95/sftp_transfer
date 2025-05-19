from dataclasses import dataclass
from datetime import datetime
from typing import List

from services.metastore.datastore.datastore import DataStore
from services.metastore.datastore.file_datastore import FileDataStore


class TransferLog:
    @dataclass
    class Entry:
        id: str
        transfer_status: str
        transfer_date: str

    datastore: DataStore
    entries: List[Entry]
    def __init__(self,datastore):
        self.datastore=datastore
        self.load()

    def insert_logs(self,input_entries : List[Entry], sync = True):
        self.entries.extend(input_entries)
        if sync:
            self.save()
        else:
            raise Exception("Not Supported")


    def save(self):
        self.datastore.save(self.entries)

    def load(self):
        items = self.datastore.load()
        self.entries = [self.Entry(**item) for item in items]

    def get_entries(self) -> List[Entry]:
        return self.entries

    def add_entries(self, entry: Entry, sync=True):
        self.entries.append(entry)
        if sync:
            self.save()
        else:
            raise Exception("Not Implemented")
