import os

import paramiko




from poc.sftp import upload_file_in_chunks
from utils.checksum import calculate_sha256


def generate_large_file(path, size_mb=20):
    with open(path, "wb") as f:
        f.write(b"\0" * size_mb * 1024 * 1024)


SFTP_USER = "foo"
SFTP_PASS = "pass"
SFTP_PORT = 2222

def test_upload_file(sftp_container):
    test_file = "test.data"
    input_path = f"./{test_file}"
    generate_large_file(input_path)
    remote_path = f"upload/{test_file}"
    downloaded_path = f"./{test_file}_downloaded"

    original_hash = calculate_sha256(input_path)

    # connect via SFTP
    transport = paramiko.Transport(("localhost", SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Upload the file
    upload_file_in_chunks(sftp,input_path,remote_path)
    # Check file exists
    files = sftp.listdir("upload")
    assert test_file in files

    # download back for checking checksum
    sftp.get(remote_path, downloaded_path)
    file_downloaded_hash = calculate_sha256(input_path)
    assert original_hash == file_downloaded_hash

    # Cleanup
    sftp.close()
    transport.close()
    os.remove(input_path)
    os.remove(downloaded_path)

