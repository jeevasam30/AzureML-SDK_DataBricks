# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 10:47:55 2023

@author: jeeva
"""

from azureml.core import Run
import argparse


# Get the context of the experiment run
new_run = Run.get_context()


# Access the Workspace
ws = new_run.experiment.workspace
print("Workspace accessed...")

# Get parameters
parser = argparse.ArgumentParser()
parser.add_argument("--testdata", type=str)
args = parser.parse_args()
print("arguments accessed and printing...")
print(args.testdata)

# Read the data from the previous step
import os
import pandas as pd

path = os.path.join(args.testdata, 'x_test.csv')
X_test = pd.read_csv(path)

path = os.path.join(args.testdata, 'y_test.csv')
Y_test = pd.read_csv(path)

path = os.path.join(args.testdata, 'y_predict.csv')
Y_predict = pd.read_csv(path)


import joblib
obj_file = os.path.join(args.testdata, 'rfcModel.pkl')
rfc = joblib.load(obj_file)
score = rfc.score(X_test, Y_test)



# Evaluate the RFC model
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test, Y_predict)

cm_dict = {"schema_type": "confusion_matrix",
           "schema_version": "v1",
           "data": {"class_labels": ["N", "Y"],
                    "matrix": cm.tolist()}
           }

new_run.log_confusion_matrix("ConfusionMatrix", cm_dict)
new_run.log("Score", score)


# Complete the run
new_run.complete()