import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

blob_service = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container = blob_service.get_container_client(CONTAINER_NAME)


def download_blob(blob_name, destination):
    blob = container.get_blob_client(blob_name)

    with open(destination, "wb") as file:
        file.write(blob.download_blob().readall())

    print(f"Downloaded {blob_name}")


def blob_exists(blob_name):
    return container.get_blob_client(blob_name).exists()