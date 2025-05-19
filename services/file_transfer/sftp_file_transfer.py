from services.file_transfer import FileTransfer
import paramiko

class SftpFileTransfer(FileTransfer):
    sftp = None

    def __init__(self,*args,**kwargs):
        transport = paramiko.Transport((kwargs["host"], kwargs["port"]))
        transport.connect(username=kwargs["user"], password=kwargs["password"])
        sftp = paramiko.SFTPClient.from_transport(transport)
        self.sftp = sftp
        self.chunk_size = kwargs.get("chunk_size", 8 * 1024 * 1024)

    def initialize(self):
        pass

    def push(self,source, destination):
        self.upload_file_in_chunks(source,destination,self.chunk_size)

    def upload_file_in_chunks(self, local_path, remote_path, chunk_size=8 * 1024 * 1024):
        with open(local_path, "rb") as f_local:
            with self.sftp.file(remote_path, "wb") as f_remote:
                print(f"start uploading file:{local_path} to {remote_path} with chunk size = {chunk_size}")
                while True:
                    chunk = f_local.read(self.chunk_size)
                    if not chunk:
                        break
                    f_remote.write(chunk)
