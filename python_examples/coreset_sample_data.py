"""
Sample a set of images using Coreset

Focus on:
JobContext.CORESET_SAMPLING
client.get_job_samples()
"""

import matplotlib.pyplot as plt

from akride import AkriDEClient, JobContext


def display_cluster_images(images: list, n_rows: int = 1, n_cols: int = 6, figure_w: int = 10, figure_h: int = 3):
    """Display a grid of n_rows x n_cols of images"""
    assert len(images) <= n_rows * n_cols
    fig = plt.figure(figsize=(figure_w, figure_h))
    for i, img in enumerate(images):
        fig.add_subplot(n_rows, n_cols, i + 1)
        plt.axis('off')
        plt.tight_layout()
        plt.imshow(img)
    print("Examples sampled after Coreset")
    # plt.show()
    plt.savefig(f"./example_core_set.jpg")  # Uncomment to save the image locally


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

# Retrieve 15% of core-set data
spec = {"percent": 15}
samples = client.get_job_samples(job, JobContext.CORESET_SAMPLING, spec)
print(f"Retrieved {len(samples)} samples")

# Display the first 6 thumbnails:
thumbnails = client.get_thumbnail_images(samples=samples[:6])
display_cluster_images(thumbnails)
print(f"Presented the samples")
