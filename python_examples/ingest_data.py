"""
Ingest images from a new dataset
"""

import time

from akride import AkriDEClient
from akride.core.enums import DataType


# Get the API_KEY from Data Explorer → Utilities → Get CLI/SDK config:
sdk_config_dict = {
  "saas_endpoint": "https://app.akridata.ai",
  "api_key": "akridata-804b6140d095:kGgXfc2qbXrgso0f5cGzuynaCiLxLZ0fc6xvRs6eFBAu0Ykd",
  "mode": "saas"
}

# Define the Data Explorer client side:
client = AkriDEClient(sdk_config_dict=sdk_config_dict)

# Register a dataset on Data Explorer:
dataset_spec = {"dataset_name": "Dataset-of-images", "data_type": DataType.IMAGE}
dataset = client.create_dataset(spec=dataset_spec)
print(f"Dataset {dataset.get_name()} created successfully with ID {dataset.get_id()}")

# Process images:
path_to_images = "/home/ubuntu/akride-examples/dataset/cat-dog-bird/"
# path_to_images = "C:\\Users\\alexb\\Documents\\akride-examples\\dataset\\cat-dog-bird\\"
#
# import os
# image_data_dir = "../dataset/cat-dog-bird/bird"
# pp = os.path.abspath(os.path.join(os.getcwd(), image_data_dir))
# print(f"processing path {pp}")
# task = client.ingest_dataset(dataset=dataset, data_directory=os.path.abspath(os.path.join(os.getcwd(), image_data_dir)))
task = client.ingest_dataset(dataset=dataset, data_directory=path_to_images)
while not task.has_completed():
    print(f"Current progress:{task.get_progress_info().percent_completed}%")
    time.sleep(5)
print("done")
