# AkriData Python Client Examples

Welcome to the AkriData Python Client (akride) Examples repository. This repository contains examples demonstrating how to use the AkriData Python client (akride) to interact with the AkriData's Data Explorer platform. **akride** allows you to seamlessly integrate AkriData's powerful data management capabilities into your Python applications.

## Getting Started

To get started with the Python client, follow these steps:

### Step 1: Sign Up for an AkriData Account

1. Visit the AkriData website at [https://akridata.ai](https://akridata.ai).

2. Click on the "Try now" button or enter the URL [https://subscriptions.akridata.ai](https://subscriptions.akridata.ai) in your browser to register for an AkriData account.

3. Once you have registered, activate your account following the instructions provided in the confirmation email.

### Step 2: Obtain the SDK Config

1. Sign in to the AkriData Data Explorer UI using your newly created account credentials.

2. Navigate to the "Utilities" section.

3. Select "Get CLI/SDK config."

4. You can copy the SDK configuration that is needed to interact with AkriData's services. Make sure to keep this configuration secure.

### Step 3: Set up your environment

#### Prerequisites

- Python version 3.8 or higher is required to run the examples in this repository.
- We recommend using a virtual environment to manage your Python dependencies.

Once you have followed the steps in the previous section, clone this repository. Once you have the SDK configuration, you can start using the client to interact with AkriData's Data Explorer platform.

## Notebooks

1. **Data Ingestion and Exploration** - [View Notebook](notebooks/akride_explore_dataset.ipynb)

   This notebook provides an example of how to ingest data into the AkriData Data Explorer application using the Python client. It shows how the client can be used to explore image data, run similarity searches, and create result sets within the AkriData platform.

2. **Analysis of an Object Classification Model** - [View Notebook](notebooks/akride_analyze_dataset.ipynb)

   This notebook shows how to ingest image data along with ground truth and prediction information of a ML model into Data Explorer, which can then be used to analyze the model accuracy in addition to data exploration.

   _Note: Make sure to follow the "Getting Started" steps to set up your environment and obtain the necessary SDK configuration before running this notebook._

## Documentation

For detailed documentation on how to use the akride client and its capabilities, please refer to the [official AkriData documentation](https://akridata-akride.readthedocs-hosted.com/en/latest/). For more information about Akridata's Data Explorer and other Akridata products, please refer to the [official product documentation](https://docs.akridata.ai/docs).

## Contributing

If you'd like to contribute to this repository, feel free to open issues, submit pull requests, or provide feedback. We welcome contributions from the community to make this repository more helpful to users.

## License

This repository is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

---

For more information about AkriData, please visit [akridata.ai](https://www.akridata.ai).
