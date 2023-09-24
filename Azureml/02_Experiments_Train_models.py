# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 16:45:02 2023

@author: jeeva
"""

from azureml.core import Workspace,Datastore,Dataset,Experiment
ws = Workspace.from_config("C:/config/config.json")
                                      
az_store=Datastore.get(workspace=ws,
                       datastore_name = 'azure_sdk_blob002') 
az_dataset = Dataset.get_by_name(ws,'loan application using SDK')
az_default_store = ws.get_default_datastore() 

#Create/access an experiment object
experiment =Experiment(workspace=ws, name='Loan_SDK_Exp01')
 
#Run an experiment using start_logging
new_run = experiment.start_logging(snapshot_directory=None) #to log into the azureml

#do you stuff here
df =az_dataset.to_pandas_dataframe()

total_observation= len(df)

null_df =df.isnull().sum()
#log to workspace the obervations

new_run.log('Total Obseravtion',total_observation)

# complete an experiment eum
new_run.complete()


