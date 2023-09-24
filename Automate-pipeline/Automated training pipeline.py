# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 17:16:31 2023

@author: jeeva
"""

#Run a script in azureml enivironmet or submit annything to the azureml

from azureml.core import Workspace,Datastore,Dataset,Experiment,ScriptRunConfig
ws = Workspace.from_config("C:/config/config.json")


from azureml.core import Environment
from azureml.core.environment import CondaDependencies

# Create the environment
myenv = Environment(name="MyEnvironment")

# Create the dependencies object
myenv_dep = CondaDependencies.create(conda_packages=['scikit-learn'])

myenv.python.conda_dependencies = myenv_dep

# Register the environment
myenv.register(ws)

from azureml.core.environment import Environment

# Assuming 'ws' is your Azure ML workspace
#test = Environment.get(workspace=ws, name='azureml_f3f7e6c5fb83d94df23933000bf02da3')

  # Use the environment created by Azure ML



from azureml.core.compute import AmlCompute
cluster_name = 'my-cluster-002'

#configuration ofcomputer cluster     
compute_config = AmlCompute.provisioning_configuration(vm_size ='Standard_A4_v2',
                                                     max_nodes = 2)

#create a cluster
#AmlCompute.create(workspace=ws, name=cluster_name, provisioning_configuration=compute_config)
from azureml.core.compute import ComputeTarget
compute_cluster = ComputeTarget.create(ws, cluster_name, compute_config)

compute_cluster.wait_for_completion()


from azureml.core.runconfig import RunConfiguration

run_config = RunConfiguration()

run_config.target = compute_cluster
run_config.environment = myenv


#Pipeline steps
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core  import PipelineData 
input_ds = ws.datasets.get('loan application using SDK')

dataFolder = PipelineData('datafolder',datastore=ws.get_default_datastore())

dataPrep_steps = PythonScriptStep(name = '01 Data Prepration',
                                  source_directory = "C:/Users/jeeva/Downloads/Miscrosoft Azure Machinelearning Course",
                                  script_name = '220 - Dataprep Pipeline.py',
                                  inputs = [input_ds.as_named_input('raw_data')],
                                  outputs= [dataFolder],
                                  runconfig=run_config,
                                  arguments = ['--datafolder',dataFolder])


# Training the model
training_steps = PythonScriptStep(name = '02 Training the model',
                                  source_directory = "C:/Users/jeeva/Downloads/Miscrosoft Azure Machinelearning Course",
                                  script_name = '220 Training Pipeline.py',
                                  inputs= [dataFolder],
                                  runconfig=run_config,
                                  arguments = ['--datafolder',dataFolder])
# Configure and build the piprline
steps =[ dataPrep_steps,training_steps]
from azureml.pipeline.core import Pipeline
new_pipeline =Pipeline(workspace = ws,steps = steps )

#Create the experiment and run the pipeline
from azureml.core import Experiment

new_experiment = Experiment(workspace = ws,name = 'PiplineExp01')

new_pipeline_run = new_experiment.submit(new_pipeline)

new_pipeline_run.wait_for_completion(show_output=True)

#"C:\Users\jeeva\Downloads\Miscrosoft Azure Machinelearning Course\220 - Dataprep Pipeline.py"
#220 Training Pipeline.py
