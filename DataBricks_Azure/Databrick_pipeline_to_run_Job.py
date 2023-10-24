# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 10:45:23 2023

@author: jeeva
"""


# Run the DatabricksStep as an AzureML Pipeline step


from azureml.core import Workspace

# Access the Workspace
ws = Workspace.from_config("./config")



# Create custom environment

from azureml.core import Environment
from azureml.core.environment import CondaDependencies

# Create the environment
myenv = Environment(name="MyEnvironment")

# Create the dependencies object
myenv_dep = CondaDependencies.create(conda_packages=['scikit-learn', 'joblib'])

myenv.python.conda_dependencies = myenv_dep

# Register the environment
myenv.register(ws)


# Create a compute cluster for pipeline
-
cluster_name = "pipeline-cluster"

# # Provisioning configuration using AmlCompute
from azureml.core.compute import AmlCompute

print("Accessing the compute cluster...")

if cluster_name not in ws.compute_targets:
    print("Creating the compute cluster with name: ", cluster_name)
    compute_config = AmlCompute.provisioning_configuration(
                                      vm_size="STANDARD_D11_V2",
                                      max_nodes=2)

    compute_cluster = AmlCompute.create(ws, cluster_name, compute_config)
    compute_cluster.wait_for_completion()
else:
    compute_cluster = ws.compute_targets[cluster_name]
    print(cluster_name, ", compute cluster found. Using it...")



# Create Run Configurations for the steps

from azureml.core.runconfig import RunConfiguration
run_config = RunConfiguration()

run_config.target = compute_cluster
run_config.environment = myenv



# Attach the Databricks Cluster as an attached compute target

from azureml.core.compute    import DatabricksCompute
from azureml.core.compute    import ComputeTarget

# Initialize the attach config parameters
db_resource_group     = "<DB Resource Group Name>"
db_workspace_name     = "<DB Workspace Name>"
db_access_token       = "<DB Workspace Access Token>"
db_compute_name       = "<DB Cluster Name>"


# Attach the Databricks compute target
if db_compute_name not in ws.compute_targets:
    print("Creating attach config for Databricks...")
    attach_config = DatabricksCompute.attach_configuration(
                            resource_group = db_resource_group,
                            workspace_name = db_workspace_name,
                            access_token = db_access_token)
    
    print("Attaching Databricks Cluster to AzureML workspace..")
    db_cluster = ComputeTarget.attach(ws,
                                      db_compute_name,
                                      attach_config)

    db_cluster.wait_for_completion(True)

else:
    print('Compute target already exists')
    db_cluster = ws.compute_targets[db_compute_name]


#data reference of Input and Output


from azureml.data.data_reference import DataReference
from azureml.pipeline.core   import PipelineData

# Create input data reference
#data_store = ws.get_default_datastore()
data_store = ws.datastores.get('adultincome')

input_data = DataReference(datastore = data_store,
                           data_reference_name = 'input')

output_data1 = PipelineData('testdata', datastore=data_store)
    


# Create the Databricks Step
from azureml.pipeline.steps import DatabricksStep
from azureml.core.databricks import PyPiLibrary

scikit_learn = PyPiLibrary(package = 'scikit-learn')
joblib       = PyPiLibrary(package = 'joblib')


notebook_path = r"<Notebook Path from the DB Cluster>"

db_step01 = DatabricksStep(name = "db_step01",
                           inputs = [input_data],
                           outputs = [output_data1],
                           num_workers = 1, 
                           notebook_path = notebook_path,
                           run_name = "db_notebook_demo",
                           compute_target = db_cluster,
                           pypi_libraries = [scikit_learn, joblib],
                           allow_reuse = False)




# Create the pipeline step to run python script


from azureml.pipeline.steps import PythonScriptStep

eval_step    = PythonScriptStep(name='Evaluate',
                                 source_directory='.',
                                 script_name='630 - Evaluate.py',
                                 inputs=[output_data1],
                                 runconfig=run_config,
                                 arguments=['--testdata', output_data1])






# Build and submit the pipeline


from azureml.pipeline.core   import Pipeline
from azureml.core            import Experiment

steps             = [db_step01, eval_step]
new_pipeline      = Pipeline(workspace=ws, steps=steps)
new_pipeline_run  = Experiment(ws, 'DB_Notebook_exp001').submit(new_pipeline)


# Wait for completion
new_pipeline_run.wait_for_completion(show_output=True)
