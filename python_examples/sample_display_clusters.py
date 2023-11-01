"""
Get a few samples from each cluster and display.

Focus on:
client.get_job_samples()
client.get_thumbnail_images()

"""
import matplotlib.pyplot as plt

from akride import AkriDEClient, JobContext


def display_cluster_images(images: list, cluster_id: int,
                           n_rows: int = 2, n_cols: int = 3, figure_size: int = 5):
    """Display a grid of n_rows x n_cols of images"""
    assert len(images) <= n_rows * n_cols
    fig = plt.figure(figsize=(figure_size, figure_size))
    for i, img in enumerate(images):
        fig.add_subplot(n_rows, n_cols, i + 1)
        plt.axis('off')
        plt.tight_layout()
        plt.imshow(img)
    print(f"Examples are ready for cluster: {cluster_id}")
    # plt.show()
    plt.savefig(f"./{cluster_id}.jpg")  # Uncomment to save the image locally


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
    cluster_images = client.get_thumbnail_images(samples)
    # display grid:
    display_cluster_images(cluster_images, cluster_id)

print("Provided examples for each cluster")
