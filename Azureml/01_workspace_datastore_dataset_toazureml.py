# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 16:33:36 2023

@author: jeeva
"""

import pandas as pd
import azureml.core
from azureml.core import Workspace,Datastore,Dataset
#creating workspace
#ws = Workspace.create(name ="Azureml-SDK-WS01",
#                      subscription_id="67cc1430-ab45-4f21-acac-7a8cbe089834",
#                     resource_group="AzuremlSDKRG01",
#                    create_resource_group=True,
#                   location="germanywestcentral")

ws = Workspace.from_config("C:/config/config.json")

#az_store = Datastore.register_azure_blob_container( workspace=ws,
                                                   #datastore_name = 'azure_sdk_blob002',
                                                   #container_name='azuremlblob01', 
                                                   #account_name='azuremlstb01sdk',
                                                  # account_key='4THLZOnjAKLsOz+P5yP1OFvNaM/rh2nFMK/x9PlljrSQZ+DveDnUdhhIq+EYqfzkE6Mh829yYz1V+AStEWnysA==')
#getting the access to datstore
#az_store=Datastore.get(workspace=ws,
                       #datastore_name = 'azure_sdk_blob002') 

#csv_path = [(az_store,'Loan_data/Loan+Approval+Prediction.csv')]
 
#registering the data in the dtastore as a datset
#loan_dataset =Dataset.Tabular.from_delimited_files(path=csv_path)  

#loan_dataset =loan_dataset.register(workspace =ws,
                                    #name= 'loan application using SDK',
                                    #create_new_version = True)   
az_store=Datastore.get(workspace=ws,
                       datastore_name = 'azure_sdk_blob002') 
az_dataset = Dataset.get_by_name(ws,'loan application using SDK')
az_default_store = ws.get_default_datastore()    

#laod a data from the Azurmel to a pandas datframe                                   

#df =az_dataset.to_pandas_dataframe()

#Upload the datframe to aureml dataset 

#df_sub=df[['Gender','Loan_Status']]

#az_ds_from_df = Dataset.Tabular.register_pandas_dataframe(dataframe=df_sub,
                                                          #target=az_store,
                                                          #name='Loan datset from pandas dataframe')


#'upload a local file directly to storage account' 
files_list = ["C:/Users/jeeva/Downloads/adultincome.csv"]
az_store.upload_files(files = files_list,
                      target_path = None,
                      overwrite = True)

#upload floder or directoty 
#az.upload(src_dirctoty = 'path',
          #target_path ='',
          #overwrite =True #in case it excist')
          
                                                                  