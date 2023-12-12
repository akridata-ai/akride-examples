"""
A complete flow using akride to analyze a model.
The flow consists of the following steps:
1. Register a dataset on Data Explorer
2. Ingest the data (images) + metadata info: ground truth + model predictions
3. Create an "Analysis" job to analyze model accuracy

Once the above has been completed, you can continue to:
4. Visualize the Confusion matrix, retrieve & view examples from a cell and their tags
5. Continue analysis on Data Explorer's interface
"""

import matplotlib.pyplot as plt
import time

from pandas import DataFrame
from sklearn.metrics import ConfusionMatrixDisplay

from akride import AkriDEClient
from akride.core.enums import DataType, JobStatisticsContext, JobContext
from akride.core.types import AnalyzeJobParams, CatalogDetails, CatalogTable, ConfusionMatrix

from display_images import display_images


# Get the API_KEY from Data Explorer → Utilities → Get CLI/SDK config:
sdk_config_dict = {
    "saas_endpoint": "https://app.akridata.ai",
    "api_key": "akridata-apikey",
    "mode": "saas",
}

# Define the Data Explorer client side:
client = AkriDEClient(sdk_config_dict=sdk_config_dict)

#######################################################################################################################
# 1. Register a dataset on Data Explorer. Avoid spaces in the dataset name:
dataset_spec = {"dataset_name": "voc-analyze", "data_type": DataType.IMAGE}
dataset = client.create_dataset(spec=dataset_spec)
print(f"Dataset {dataset.get_name()} created successfully with ID {dataset.get_id()}")

# If a dataset already exists, connect to it, for example:
# dataset = client.get_dataset_by_name(name="cats-dogs-birds")

#######################################################################################################################
# 2.1 Process images:
# path_to_images = "../dataset/voc-analyze/"
path_to_images = "C:\\Users\\alexb\\Documents\\akride-examples\\dataset\\voc-analyze\\"
task = client.ingest_dataset(dataset=dataset, data_directory=path_to_images, async_req=True)

while not task.has_completed():
    print(f"Current progress:{task.get_progress_info().percent_completed}%")
    time.sleep(5)
print("Dataset ingestion done")

# 2.2 Process catalog data:
catalog_table_name = "voc_catalog_info"
# catalog_csv_path = "../dataset/voc-analyze/catalog/voc_catalog.csv"
catalog_csv_path = "C:\\Users\\alexb\\Documents\\akride-examples\\dataset\\voc-analyze\\catalog\\voc_catalog.csv"
is_successful: bool = client.import_catalog(dataset=dataset,
                                            csv_file_path=catalog_csv_path,
                                            file_name_column="file_path(string)",
                                            table_name=catalog_table_name,
                                            create_view=True)
if is_successful:
    print(f"Catalog imported {catalog_table_name} created successfully, view {catalog_table_name}_primary_view created")
else:
    print(f"View {catalog_table_name} creation failed.")
# Display the table:
catalog_view = CatalogTable(table_name="voc_catalog_info_primary_view", is_view=True)
client.get_all_columns(dataset=dataset, table=catalog_view)

#######################################################################################################################
# 3. Create a job and wait for completion. Job name must be at least 3 characters long:
job_name = "voc-analyze"
job_spec = client.create_job_spec(
    dataset=dataset,
    job_name=job_name,
    catalog_table=catalog_view,
    analyze_params=AnalyzeJobParams(
        catalog_config=CatalogDetails(
            score_column="voc_catalog_info_pd_score(float)",
            ground_truth_class_column="voc_catalog_info_gt_class(string)",
            prediction_class_column="voc_catalog_info_pd_class(string)",
            ground_truth_coordinates_column="voc_catalog_info_gt_box(string)",
            prediction_coordinates_column="voc_catalog_info_pd_box(string)",
        )
    ),
)
job = client.create_job(spec=job_spec)
while True:
    job = client.get_job_by_name(job_name.upper())
    if job.info.status in ["READY", "FAILED"]:  # type: ignore
        if job.info.status == "FAILED":  # type: ignore
            print(f"{job.get_name()} is in failed state. See logs for more info.")
        break
    else:
        print("Waiting for job completion")
        time.sleep(5)

print(f"Ready to explore - {job.get_name()} with {job.info.to_dict()['tunables_default']['max_clusters']} clusters")

#######################################################################################################################
# 4. The confusion matrix for job analysis:
conf_matrix: ConfusionMatrix = \
    client.get_job_statistics(job=job, context=JobStatisticsContext.CONFUSION_MATRIX)  # type: ignore

# 4.1. Display the matrix:
disp = ConfusionMatrixDisplay(conf_matrix.data, display_labels=conf_matrix.labels)
_, ax = plt.subplots(figsize=(25, 25))
disp.plot(ax=ax)

# 4.2. Get 2 examples of incorrect prediction:
spec = {"true_label": "sofa", "predicted_label": "chair"}
samples = client.get_job_samples(job, JobContext.CONFUSION_MATRIX_CELL, spec)
thumbnails = client.get_thumbnail_images(samples[:2])

print("Display the result-set images:")
# set save_file=None to view the image without saving:
display_images(thumbnails, n_rows=1, n_cols=2, figure_w=5, figure_h=5, save_file="./confusion_matrix_cell.jpg")

# 4.3. Get catalog tag for the above samples:
df: DataFrame = client.get_catalog_tags(samples)
print(df.head())

#######################################################################################################################
# 5. Continue to analyze model accuracy within Data Explorer following the below url:
url = client.get_job_display_panel(job)
print(url)
# Note: url requires login into Data Explorer
