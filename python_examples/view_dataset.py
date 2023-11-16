"""
Get a URL into Data Explorer for the data visualization.

Focus on:
client.get_job_display_panel()
"""

from akride import AkriDEClient


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

# Get the URL for the job in Data Explorer:
url = client.get_job_display_panel(job)
print(url)

# NOTE:
# 1. Login into your Data Explorer account
# 2. The URL is your dataset visualization page
