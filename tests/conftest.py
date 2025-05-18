# conftest.py
import pytest
import docker
import time
import os


SFTP_USER = "foo"
SFTP_PASS = "pass"
SFTP_PORT = 2222

@pytest.fixture(scope="session")
def sftp_container():
    client = docker.from_env()
    container = client.containers.run(
        "atmoz/sftp",
        f"{SFTP_USER}:{SFTP_PASS}:::upload",
        ports={"22/tcp": SFTP_PORT},
        detach=True,
    )

    # Wait for SFTP server to be ready
    time.sleep(3)

    yield container

    # Cleanup
    container.remove(force=True)