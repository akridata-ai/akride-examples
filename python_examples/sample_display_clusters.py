"""
After creating a visualization of a dataset, get a few samples from each cluster and display them.

Focus on:
client.get_job_samples()
client.get_thumbnail_images()
"""

from akride import AkriDEClient, JobContext

from display_images import display_images

# Get the API_KEY from Data Explorer → Utilities → Get CLI/SDK config:
sdk_config_dict = {
  "saas_endpoint": "https://app.akridata.ai",
  "api_key": "akridata-804b6140d095:kGgXfc2qbXrgso0f5cGzuynaCiLxLZ0fc6xvRs6eFBAu0Ykd",
  "mode": "saas"
}
# Define the Data Explorer client side:
client = AkriDEClient(sdk_config_dict=sdk_config_dict)

# Retrieve the job by name:
job = client.get_job_by_name("data-explore".upper())
print(f"Got job - {job.get_name()}")

# Get number of clusters to sample from:
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
    print(f"Examples for cluster {cluster_id}")
    display_images(thumbnails, n_rows=2, n_cols=3, figure_w=5, figure_h=5, save_file=None)
    # display_images(thumbnails, n_rows=2, n_cols=3, figure_w=5, figure_h=5, save_file="./" + str(cluster_id) + ".jpg")

print("Provided examples for each cluster")
