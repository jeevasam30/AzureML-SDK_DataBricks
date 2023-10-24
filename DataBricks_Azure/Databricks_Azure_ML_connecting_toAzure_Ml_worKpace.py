# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 10:42:23 2023

@author: jeeva
"""
#Attaching databricks Cluster to Azure Ml workSpace
from azureml.core import Workspace
from azureml.core.compute import DatabricksCompute, ComputeTarget

# Access the Workspace
print("Accessing the AzureML workspace...")
ws = Workspace.from_config("./config")


# Create the configuration information of the cluster
print("Initializing the parameters...")
db_resource_group     = "databricksRG001"
db_workspace_name     = "databricksWS001"
db_access_token       = "######################"
db_compute_name       = "mydbcluster001"


if db_compute_name not in ws.compute_targets:
    print("Creating Configuration for the DB Cluster....")
    attach_config = DatabricksCompute.attach_configuration(
                                resource_group = db_resource_group,
                                workspace_name = db_workspace_name,
                                access_token = db_access_token)
    
    print("Attaching the compute target....")
    db_cluster = ComputeTarget.attach(ws, 
                                      db_compute_name, 
                                      attach_config)
    
    db_cluster.wait_for_completion(True)

else:
    print("Compute target exists...")
    db_cluster = ws.compute_targets[db_compute_name]
