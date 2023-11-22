"""
Sample a set of images using Coreset - preserving small clusters.

Focus on:
JobContext.CORESET_SAMPLING
client.get_job_samples()
"""

from akride import AkriDEClient, JobContext

from display_images import display_images

# Get the API_KEY from Data Explorer → Utilities → Get CLI/SDK config:
sdk_config_dict = {
    "saas_endpoint": "https://app.akridata.ai",
    "api_key": "akridata-apikey",
    "mode": "saas",
}
# Define the Data Explorer client side:
client = AkriDEClient(sdk_config_dict=sdk_config_dict)

# Retrieve the job by name:
job = client.get_job_by_name("data-explore".upper())
print(f"Got job - {job.get_name()}")

# Apply coreset sampling to get 15% of the images:
spec = {"percent": 15}
samples = client.get_job_samples(job, JobContext.CORESET_SAMPLING, spec)
print(f"Retrieved {len(samples)} samples")

# Display the first 6 thumbnails:
thumbnails = client.get_thumbnail_images(samples=samples[:6])
print("Examples after Core-set:")
display_images(
    thumbnails, n_rows=1, n_cols=6, figure_w=10, figure_h=3, save_file=None
)
# display_images(thumbnails, n_rows=1, n_cols=6, figure_w=10, figure_h=3, save_file="./coreset.jpg")
