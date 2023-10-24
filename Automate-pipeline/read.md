# Automated Machine Learning Pipeline

This repository contains Python scripts for setting up an automated machine learning pipeline using Azure Machine Learning services. The pipeline consists of the following steps:

1. **Data Preparation**: The script `220 - Dataprep Pipeline.py` handles the data preparation step of the pipeline. It includes tasks such as reading the input dataset, cleaning missing data, creating dummy variables, and saving the prepared data.

2. **Training the Model**: The script `220 Training Pipeline.py` focuses on training a logistic regression model using the prepared data. It covers tasks such as splitting the data, building the model, and evaluating its performance.

3. **Pipeline Configuration**: The pipeline steps are configured and built using Azure ML's pipeline functionality.

## Usage

To run this pipeline in your Azure ML workspace, follow these steps:

1. **Set up Your Azure ML Workspace**: Ensure you have an Azure ML workspace and have configured it properly.

2. **Create an Azure ML Compute Cluster**: Set up a compute cluster for running the pipeline steps. You can adjust the `cluster_name` and `compute_config` in the scripts as per your requirements.

3. **Configure and Build the Pipeline**: Update the `source_directory` and `script_name` in the `PythonScriptStep` objects to point to the correct locations of your scripts.

4. **Create an Experiment**: Define a new experiment in your Azure ML workspace (e.g., `PiplineExp01`).

5. **Submit the Pipeline**: Use the experiment to submit the pipeline for execution.

For detailed information on each step, refer to the individual scripts and comments within them.

## Scripts

- [`220 - Dataprep Pipeline.py`](path_to_script): Data preparation step of the pipeline.
- [`220 Training Pipeline.py`](path_to_script): Training the machine learning model.

## Requirements

- Azure ML Workspace
- Python
- Azure ML SDK

## References

- [Azure Machine Learning Documentation](https://docs.microsoft.com/azure/machine-learning/)

