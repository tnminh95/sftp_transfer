from typing import List
from dataclasses import dataclass, asdict

from services.file_transfer import FileTransfer
from services.metastore.file_registry import FileRegistry
from services.metastore.transfer_logs import TransferLog
import random
from datetime import datetime
import os
import json
class FileTransferAgent:
    def __init__(self, file_transfer: FileTransfer, file_registry: FileRegistry, transfer_logs: TransferLog, tmp_path = "./"):
        self.file_transfer = file_transfer
        self.file_registry = file_registry
        self.transfer_logs = transfer_logs
        self.tmp_path = tmp_path

    def get_list_file_upload(self, input_date: str) -> List[FileRegistry.Entry]:
        f_entries = self.file_registry.get_entries()
        t_logs = self.transfer_logs.get_entries()
        log_ids = [log.id for log in t_logs]
        result =[]
        for file in f_entries:
            if file.updated_date == input_date:
                if file.id not in log_ids:
                    result.append(file)
                    continue
                for log in t_logs:
                    if log.id == file.id and log.transfer_status in ["failed"]:
                        result.append(file)

        return result

    def make_control_file(self,entries):
        seed = random.randint(0, 9)
        timestamp = datetime.now().timestamp()
        file_id = f"{str(timestamp)}_{seed}"
        control_file_path = os.path.join(self.tmp_path,f"{file_id}.json")

        with open(control_file_path, 'w', encoding='utf-8') as file:
            content = json.dumps([asdict(entry) for entry in entries], indent=4)
            file.write(content)
        return control_file_path


    def run_upload_file(self,destination_file_path, destination_control_file_path, input_date):
        entries = self.get_list_file_upload(input_date)
        control_file_path = self.make_control_file(entries)
        for file in entries:
            dest_file = os.path.join(destination_file_path,file.path.split("/")[-1])
            self.file_transfer.push(file.path,dest_file)

        dest_file = os.path.join(destination_control_file_path, control_file_path.split("/")[-1])
        self.file_transfer.push(control_file_path,dest_file)

