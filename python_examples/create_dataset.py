"""
Create a dataset in Data Explorer, but without adding or ingesting any data.

Focus on:
client.create_dataset()
"""

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
}  # Use DataType.VIDEO for videos
dataset = client.create_dataset(spec=dataset_spec)
print(
    f"Dataset {dataset.get_name()} created successfully with ID {dataset.get_id()}"
)
