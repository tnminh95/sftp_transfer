
def upload_file_in_chunks(sftp, local_path, remote_path,chunk_size=8*1024*1024):
    with open(local_path, "rb") as f_local:
        with sftp.file(remote_path, "wb") as f_remote:
            print(f"start uploading file:{local_path} to {remote_path} with chunk size = {chunk_size}")
            while True:
                chunk = f_local.read(chunk_size)
                if not chunk:
                    break
                f_remote.write(chunk)