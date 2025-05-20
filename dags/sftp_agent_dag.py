import os
import sys
sys.path.append('/opt/airflow/sftp_transfer')
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from services.file_transfer.agent import FileTransferAgent
from services.file_transfer.sftp_file_transfer import SftpFileTransfer
from services.metastore.datastore.file_datastore import FileDataStore
from services.metastore.file_registry import FileRegistry
from services.metastore.transfer_logs import TransferLog



# connection to sftp db, for testing only
SFTP_USER = "foo"
SFTP_PASS = "pass"
SFTP_PORT = 2222


def sftp_agent():
    data_date = "2025-05-11"  # hard coded for testing, in production it's previous date
    file_registry = FileRegistry(FileDataStore(file_path="resources/data/file_registry.json"))
    transfer_log = TransferLog(FileDataStore(file_path="resources/data/transfer_logs.json"))
    sftp_transfer = SftpFileTransfer(host="localhost", port=SFTP_PORT, user=SFTP_USER, password=SFTP_PASS)
    sftp_agent = FileTransferAgent(sftp_transfer, file_registry, transfer_log)
    sftp_agent.run_upload_file(f"upload/data/", f"upload/control/", data_date)


# Define the DAG
with DAG(
        dag_id='sftp_agent',
        start_date=datetime(2025, 5, 19),
        schedule_interval='@daily',
        catchup=False,
) as dag:
    sftp_agent = PythonOperator(
        task_id='sftp_agent',
        python_callable=sftp_agent,
    )

