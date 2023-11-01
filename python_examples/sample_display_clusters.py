import matplotlib.pyplot as plt

from PIL import Image

from akride import AkriDEClient, JobContext


def display_grid(n_rows: int, n_cols: int, images: list[Image.Image], size: int, cluster_id: int):
    """Display a grid of n_rows x n_cols of images"""
    assert len(images) <= n_rows * n_cols
    fig = plt.figure(figsize=(size, size))
    for i, img in enumerate(images):
        fig.add_subplot(n_rows, n_cols, i + 1)
        plt.axis('off')
        plt.tight_layout()
        plt.imshow(img)
    # plt.show()
    plt.savefig(f"./{cluster_id}.jpg")


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

# Get number of clusters to sample from:
num_clusters = job.info.to_dict()["tunables_default"]["max_clusters"]

# Get a few examples from each cluster and display in a grid:
grid_n_rows: int = 2
grid_n_cols: int = 3
max_count = grid_n_rows * grid_n_cols  # number of examples to get from a cluster

for cluster_id in range(1, num_clusters + 1):
    # Set the cluster ID:
    spec = {"cluster_id": cluster_id, "max_count": max_count}
    # Get thumbnails of the chosen samples:
    samples = client.get_job_samples(job, JobContext.CLUSTER_RETRIEVAL, spec)  # type: ignore
    cluster_images = client.get_thumbnail_images(samples)
    # display grid:
    display_grid(grid_n_rows, grid_n_cols, cluster_images, 5, cluster_id)
