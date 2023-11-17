"""
Ingest images from a new dataset to create a representation of each image.
After this step, we can visualize, explore, sample the data and much more.

Focus on:
client.ingest_dataset()
"""

import time

from akride import AkriDEClient
from akride.core.enums import DataType


# Get the API_KEY from Data Explorer → Utilities → Get CLI/SDK config:
sdk_config_dict = {
    "saas_endpoint": "https://app.akridata.ai",
    "api_key": "akridata-apikey",
    "mode": "saas",
}

# Define the Data Explorer client side:
client = AkriDEClient(sdk_config_dict=sdk_config_dict)

# Register a dataset on Data Explorer:
dataset_spec = {
    "dataset_name": "Dataset-of-images",
    "data_type": DataType.IMAGE,
}
dataset = client.create_dataset(spec=dataset_spec)
print(
    f"Dataset {dataset.get_name()} created successfully with ID {dataset.get_id()}"
)

# Process images:
path_to_images = "/home/ubuntu/akride-examples/dataset/cat-dog-bird/"
task = client.ingest_dataset(dataset=dataset, data_directory=path_to_images)
while not task.has_completed():
    print(f"Current progress:{task.get_progress_info().percent_completed}%")
    time.sleep(5)
print("Dataset ingestion done")
