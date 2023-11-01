"""
Create a visual search.

Focus on:
akride.JobContext.SIMILARITY_SEARCH
client.get_job_samples()

NOTE the samples needed for the spec:
    positive_samples
    negative_samples
"""
import os

import akride

from akride import AkriDEClient


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

# Ensure that the image paths used here match the image paths used for ingest
positive_samples = [os.path.abspath(os.path.join(os.getcwd(), sample)) for sample in POS_IMAGE_SAMPLES]
negative_samples = [os.path.abspath(os.path.join(os.getcwd(), sample)) for sample in NEG_IMAGE_SAMPLES]

spec = {'positive_samples': positive_samples, 'negative_samples': negative_samples}
samples = client.get_job_samples(job, akride.JobContext.SIMILARITY_SEARCH, spec)
