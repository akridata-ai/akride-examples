"""
Create a visual search based on:
    positive_samples - we want to see images like those
    negative_samples - we don't want to see images like those

To emphasize:
The search is run on the images' content, not any metadata associated with the images.

Focus on:
akride.JobContext.SIMILARITY_SEARCH
client.get_job_samples()
"""

import os

from akride import AkriDEClient, JobContext

from display_images import display_images

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

print("Displaying the results:")
display_images(thumbnails, n_rows=4, n_cols=4, figure_w=5, figure_h=5, save_file=None)
# display_images(thumbnails, n_rows=4, n_cols=4, figure_w=5, figure_h=5, save_file="search.jpg")
