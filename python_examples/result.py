"""
Create a result set for further data curation.
Resultset is the way Data Explorer provides result to user in a 'read only' environment.

Focus on:
client.create_resultset()
client.get_resultset_samples()
"""
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

# Use Coreset sampling to choose images to add to a result-set:
samples = client.get_job_samples(job, JobContext.CORESET_SAMPLING, {"percent": 10})  # type: ignore

# Create a result-set:
result_set_spec = {"job": job, "name": "result-dog-search", "samples": samples}
resultset = client.create_resultset(result_set_spec)

# An existing result-set can be retrieved by name as below:
result_set_retrieved = client.get_resultset_by_name("result-dog-search")

# Get images from the resultset:
result_set_samples = client.get_resultset_samples(resultset=resultset)  # type: ignore
thumbnails = client.get_thumbnail_images(result_set_samples)
print(f"Retrieved {len(thumbnails)} images from result-set")

print("Display the result-set images:")
display_images(thumbnails, n_rows=3, n_cols=3, figure_w=5, figure_h=5, save_file=None)
# display_images(thumbnails, n_rows=3, n_cols=3, figure_w=5, figure_h=5, save_file="./result_set.jpg")
