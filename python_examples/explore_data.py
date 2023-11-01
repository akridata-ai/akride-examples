"""
Exploring the data in a given dataset
"""

import time

from akride import AkriDEClient


# Get the API_KEY from Data Explorer → Utilities → Get CLI/SDK config:
sdk_config_dict = {
  "saas_endpoint": "https://app.akridata.ai",
  "api_key": "akridata-804b6140d095:kGgXfc2qbXrgso0f5cGzuynaCiLxLZ0fc6xvRs6eFBAu0Ykd",
  "mode": "saas"
}
# Define the Data Explorer client side:
client = AkriDEClient(sdk_config_dict=sdk_config_dict)

# Get dataset using dataset name
dataset = client.get_dataset_by_name(name="Dataset-of-images")
print(f"Connected to {dataset.get_name()}, ID: {dataset.get_id()}")

# Create a job and wait for completion:
job_name = "data-explore"
job_spec = client.create_job_spec(dataset=dataset, job_name=job_name)
job = client.create_job(spec=job_spec)
while True:
    job = client.get_job_by_name(job_name.upper())
    if job.info.status in ["READY", "FAILED"]:  # type: ignore
        if job.info.status == "READY":  # type: ignore
            print(f"{job.get_name()} is ready for visualization with "
                  f"{job.info.to_dict()['tunables_default']['max_clusters']} clusters")
        else:
            print(f"{job.get_name()} is in failed state")
            break
    else:
        print("Waiting for job completion")
        time.sleep(5)
print(f"Ready to explore {job_name}")