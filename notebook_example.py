# DE-demo
# {
#   "saas_endpoint": "https://app.akridata.ai",
#   "api_key": "akridata-cd59c79bac21:rdhWdbUcop+jK84eELaGTxUkAvdkj1Z/gZPHV+0j65qAn94G",
#   "mode": "saas"
# }
import os

import glob
import matplotlib.pyplot as plt
import random
import string
import time

from IPython.core.display import Image

import akride
from akride import AkriDEClient, JobContext
from akride.core.enums import DataType, EmbedAlgoType, JobType, ClusterAlgoType


def find_n_images(directory, n):
    image_files = []

    # Recursively search for image files in the directory and its subdirectories.
    for root, _, files in os.walk(directory):
        image_files.extend(glob.glob(os.path.join(root, '*.jpg')))
        # todo - do we need these?
        image_files.extend(glob.glob(os.path.join(root, '*.jpeg')))
        image_files.extend(glob.glob(os.path.join(root, '*.png')))
        # Add more extensions if needed.

    # Return the first 'n' image files or all if there are fewer than 'n'.
    res = [os.path.abspath(img_file) for img_file in image_files[:n]]
    return res


# Utility function
def display_grid(nrows, ncols, imgs, size):
    assert len(imgs) <= nrows*ncols
    fig = plt.figure(figsize=(size, size))
    for i, img in enumerate(imgs):
        fig.add_subplot(nrows, ncols, i + 1)
        plt.axis('off')
        plt.tight_layout()
        plt.imshow(img)
    plt.show()


SAAS_ENDPOINT = "https://app.akridata.ai"
# Get the sdk config by signing in to Data Explorer UI and navigating to Utilities → Get CLI/SDK config
API_KEY = "akridata-cd59c79bac21:rdhWdbUcop+jK84eELaGTxUkAvdkj1Z/gZPHV+0j65qAn94G"

sdk_config_dict = {
  "saas_endpoint": SAAS_ENDPOINT,
  "api_key": API_KEY,
  "mode": "saas"
}

# Absolute/relative path to the directory which consists of images
IMAGE_DATA_DIR = "C:\\Users\\alexb\\Documents\\akride-examples\\dataset\\cat-dog-bird\\"
# Name of the dataset
DATASET_NAME = "cats-dogs-birds"

# Max images to use in the explore job
MAX_IMAGES_IN_JOB = 100

client = AkriDEClient(sdk_config_dict=sdk_config_dict)

# todo do we need the random suffix?
# # Create a random string of length 5 to enable re-run
# rand_prefix = ''.join(random.choices(string.ascii_uppercase, k=5))
# if DATASET_NAME == "cats-dogs-birds":
#     dataset_name = f"{DATASET_NAME}-{rand_prefix}"
# else:
#     dataset_name = DATASET_NAME
dataset_name = f"{DATASET_NAME}--EXAMPLE"
dataset_spec = {"dataset_name": dataset_name, "data_type": DataType.IMAGE}

# todo create_dataset - return "entity", not Dataset, as expected by "ingest_dataset"
dataset = client.create_dataset(spec=dataset_spec)
print(f"Dataset {dataset.get_name()} created successfully with ID {dataset.get_id()}")

data_directory = os.path.abspath(os.path.join(os.getcwd(), IMAGE_DATA_DIR))
print(data_directory)

task = client.ingest_dataset(dataset=dataset, data_directory=os.path.abspath(os.path.join(os.getcwd(), IMAGE_DATA_DIR)))
while not task.has_completed():
    print(f"Current progress:{task.get_progress_info().percent_completed}%")
    time.sleep(5)

# Get dataset using dataset name
# todo create_dataset - return "entity" or None, not Dataset, as expected by "get_dataset_by_name"
ds = client.get_dataset_by_name(name=dataset_name)
print("got data set by name")
# todo do we need the random prefix?
rand_prefix = ''.join(random.choices(string.ascii_uppercase, k=5))
job_name = f"{dataset_name}-explore-{rand_prefix}".upper()
print(f"job name - {job_name}")
job_spec = client.create_job_spec(dataset=ds,
                                  job_type=JobType.EXPLORE,
                                  job_name=job_name,
                                  embed_algo=EmbedAlgoType.UMAP,
                                  cluster_algo=ClusterAlgoType.HDBSCAN,
                                  catalog_name="primary",  # todo - what is primary?
                                  max_images=MAX_IMAGES_IN_JOB)
print("got job spec")
job = client.create_job(spec=job_spec)
print("created the job")

while True:
    job = client.get_job_by_name(job_name.upper())
    if job.info.status in ["READY", "FAILED"]:  # type: ignore
        # todo "status" appears unresolved reference
        if job.info.status == "READY":
            print(f"{job.get_name()} is ready for visualization with "
                  f"{job.info.to_dict()['tunables_default']['max_clusters']} clusters")
                  # todo - what are 'tunables_default', 'max_clusters'?
        else:
            print(f"{job.get_name()} is in failed state")
            # exit(1)
            break
    else:
        print("Waiting for job completion")
        time.sleep(5)

nrows = 2
ncols = 3
max_count = nrows * ncols
max_clusters = job.info.to_dict()["tunables_default"]["max_clusters"]
for cluster_id in range(1, max_clusters + 1):
    spec = {
        "cluster_id": cluster_id,
        "max_count": max_count,
    }
    # todo: spec - unexpected type - it seems that the expected types inherit from dict
    samples = client.get_job_samples(
        job, JobContext.CLUSTER_RETRIEVAL, spec
    )

    if not len(samples):
        break
    imgs = client.get_thumbnail_images(samples)
    print(f"cluster {cluster_id}")
    display_grid(nrows, ncols, imgs, 5)


spec = {"percent": 10}  # Retrieve 10% of core-set data
samples = client.get_job_samples(
    job, JobContext.CORESET_SAMPLING, spec)
thumbnails = client.get_thumbnail_images(samples=samples[:6])
print(f"Retrieved {len(samples)} samples")

print("Showing a subset of data")
display_grid(nrows=1, ncols=6, imgs=thumbnails, size=10)

# Randomly select a positive and negative sample
positive_sample, negative_sample = find_n_images(directory=IMAGE_DATA_DIR, n=2)

print("Running a similarity search for the below image")
Image(filename=positive_sample, height=500, width=500)

spec = {'positive_samples': [positive_sample], 'negative_samples': [negative_sample]}
samples = client.get_job_samples(
    job, akride.JobContext.SIMILARITY_SEARCH, spec)

thumbnails = client.get_thumbnail_images(samples=samples)

print(f"Retrieved {len(thumbnails)} images")

display_grid(4, 4, thumbnails, 10)

result_set_name = "DOGS-RESULTSET-FROM-SIM-SEARCH"
result_set_spec = {"job": job, "name": result_set_name, "samples": samples}
result_set = client.create_resultset(result_set_spec)

result_set = client.get_resultset_by_name(result_set_name)

result_set_samples = client.get_resultset_samples(resultset=result_set)  # type: ignore
result_set_images = client.get_thumbnail_images(result_set_samples)
display_grid(4, 4, result_set_images, 10)
