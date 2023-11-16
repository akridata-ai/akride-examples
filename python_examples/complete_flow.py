"""
A complete flow using akride to process a dataset.
The flow consists of the following steps:
1. Register a dataset on Data Explorer
2. Ingest the data (images)
3. Explore the dataset via an "Exploration" job

Once the above has been completed, you can process a dataset with the below:
4. Visualize the dataset on a 2D plane
5. Sample the dataset via Coreset (and other sampling methods)
6. Apply visual search through the dataset, based on image content

Finally, create a result-set to save the curated data
"""

import os
import time

from akride import AkriDEClient, JobContext
from akride.core.enums import DataType

from display_images import display_images


# Get the API_KEY from Data Explorer → Utilities → Get CLI/SDK config:
sdk_config_dict = {
  "saas_endpoint": "https://app.akridata.ai",
  "api_key": "akridata-804b6140d095:kGgXfc2qbXrgso0f5cGzuynaCiLxLZ0fc6xvRs6eFBAu0Ykd",
  "mode": "saas"
}

# Define the Data Explorer client side:
client = AkriDEClient(sdk_config_dict=sdk_config_dict)

#######################################################################################################################
# 1. Register a dataset on Data Explorer. Avoid spaces in the dataset name:
dataset_spec = {"dataset_name": "cats-dogs-birds", "data_type": DataType.IMAGE}
dataset = client.create_dataset(spec=dataset_spec)
print(f"Dataset {dataset.get_name()} created successfully with ID {dataset.get_id()}")

# If a dataset already exists, connect to it, for example:
# dataset = client.get_dataset_by_name(name="cats-dogs-birds")

#######################################################################################################################
# 2. Process images:
path_to_images = "/home/ubuntu/akride-examples/dataset/cat-dog-bird/"
task = client.ingest_dataset(dataset=dataset, data_directory=path_to_images)
while not task.has_completed():
    print(f"Current progress:{task.get_progress_info().percent_completed}%")
    time.sleep(5)
print("Dataset ingestion done")

#######################################################################################################################
# 3. Create a job and wait for completion. Job name must be at least 3 characters long:
job_name = "cats-dogs-birds-explore"
job_spec = client.create_job_spec(dataset=dataset, job_name=job_name)
job = client.create_job(spec=job_spec)
while True:
    job = client.get_job_by_name(job_name.upper())
    if job.info.status in ["READY", "FAILED"]:  # type: ignore
        if job.info.status == "FAILED":  # type: ignore
            print(f"{job.get_name()} is in failed state. See logs for more info.")

        break
    else:
        print("Waiting for job completion")
        time.sleep(5)

print(f"Ready to explore - {job.get_name()} with {job.info.to_dict()['tunables_default']['max_clusters']} clusters")

# If job exists, you can get it via name:
# job = client.get_job_by_name("cats-dogs-birds-explore".upper())

#######################################################################################################################
# 4. Visualize the data

# Visualize the dataset on a 2D plane within Data Explorer following the below url:
url = client.get_job_display_panel(job)
print(url)
# Note: url requires login into Data Explorer

# Alternative, retrieve images from each cluster:
# Get number of clusters to sample from
num_clusters = job.info.to_dict()["tunables_default"]["max_clusters"]
print(f"Data has {num_clusters} clusters")

# Number of samples to get from each cluster:
max_count = 5

for cluster_id in range(1, num_clusters + 1):
    # Set the cluster ID:
    spec = {"cluster_id": cluster_id, "max_count": max_count}
    # Get thumbnails of the chosen samples:
    samples = client.get_job_samples(job, JobContext.CLUSTER_RETRIEVAL, spec)  # type: ignore
    thumbnails = client.get_thumbnail_images(samples)
    # display grid:
    print(f"Examples for cluster {cluster_id}")  # set save_file=None to view the image without saving:
    display_images(thumbnails, n_rows=2, n_cols=3, figure_w=5, figure_h=5, save_file="./" + str(cluster_id) + ".jpg")

print("Provided examples for each cluster")

#######################################################################################################################
# 5. Apply coreset sampling to get 15% of the images:
spec = {"percent": 15}
samples = client.get_job_samples(job, JobContext.CORESET_SAMPLING, spec)
thumbnails = client.get_thumbnail_images(samples=samples[:6])
print(f"Retrieved {len(samples)} samples")

print("Showing a subset of data:")  # set save_file=None to view the image without saving:
display_images(thumbnails, n_rows=1, n_cols=6, figure_w=10, figure_h=3, save_file="./coreset.jpg")

#######################################################################################################################
# 6. Apply visual search, i.e. based on the below chosen query images:

# Positive Image samples for similarity search - you want results similar to them:
pos_images = ["../dataset/cat-dog-bird/dog/109.jpg", "../dataset/cat-dog-bird/dog/1073.jpg"]
# Negative Image Samples for similarity search - you don't want results similar to them:
neg_images = ["../dataset/cat-dog-bird/cat/1076.jpg", "../dataset/cat-dog-bird/bird/1080.jpg"]

# Ensure that the image paths used here match the image paths used for ingest:
positive_samples = [os.path.abspath(os.path.join(os.getcwd(), sample)) for sample in pos_images]
negative_samples = [os.path.abspath(os.path.join(os.getcwd(), sample)) for sample in neg_images]
print("Pos and Neg examples:")
print(positive_samples)
print(negative_samples)

spec = {'positive_samples': positive_samples, 'negative_samples': negative_samples}
samples = client.get_job_samples(job, JobContext.SIMILARITY_SEARCH, spec)

thumbnails = client.get_thumbnail_images(samples=samples)
print(f"Retrieved {len(thumbnails)} images")

print("Displaying the results:")  # set save_file=None to view the image without saving:
display_images(thumbnails, n_rows=4, n_cols=4, figure_w=5, figure_h=5, save_file="./search.jpg")

#######################################################################################################################
# Save the curated data into a result-set for further processing:
result_set_spec = {"job": job, "name": "result-dog-search", "samples": samples}
resultset = client.create_resultset(result_set_spec)

# An existing result-set can be retrieved by name as below:
# resultset = client.get_resultset_by_name("result-dog-search")

# Get images from the resultset:
result_set_samples = client.get_resultset_samples(resultset=resultset)  # type: ignore
thumbnails = client.get_thumbnail_images(result_set_samples)
print(f"Retrieved {len(thumbnails)} images from result-set")

print("Display the result-set images:")  # set save_file=None to view the image without saving:
display_images(thumbnails, n_rows=4, n_cols=4, figure_w=5, figure_h=5, save_file="./result_set.jpg")
