from services.file_transfer.agent import FileTransferAgent
from services.file_transfer.sftp_file_transfer import SftpFileTransfer
from services.metastore.datastore.file_datastore import FileDataStore
from services.metastore.file_registry import FileRegistry
from services.metastore.transfer_logs import TransferLog

SFTP_USER = "foo"
SFTP_PASS = "pass"
SFTP_PORT = 2222


def test_upload_file_to_sftp_server(sftp_container):
    file_registry = FileRegistry(FileDataStore(file_path="resources/data/file_registry.json"))
    transfer_log = TransferLog(FileDataStore(file_path="resources/data/transfer_logs.json"))
    sftp_transfer = SftpFileTransfer(host="localhost",port=SFTP_PORT,user=SFTP_USER,password=SFTP_PASS)
    sftp_agent = FileTransferAgent(sftp_transfer,file_registry,transfer_log)
    sftp_agent.run_upload_file(f"upload/data/",f"upload/control/","2025-05-11")