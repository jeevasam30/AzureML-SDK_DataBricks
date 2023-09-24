# --------------------------------------------------------------
# Data preparation step of the pipeline run
# --------------------------------------------------------------

from azureml.core import Run


# Get the run context
new_run = Run.get_context()


# Get the workspace from the run
ws = new_run.experiment.workspace


# --------------------------------------------------------
# Do your stuff here
# --------------------------------------------------------

import pandas as pd

# Read the input dataset
df = new_run.input_datasets['raw_data'].to_pandas_dataframe()
# Select columns from the dataset
LoanPrep = df[["Married", 
             "Education",
             "Self_Employed",
             "ApplicantIncome",
             "LoanAmount",
             "Loan_Amount_Term",
             "Credit_History",
             "Loan_Status"
             ]]

all_cols = LoanPrep.columns


# Check the missing values
dataNull = LoanPrep.isnull().sum()

# Clean Missing Data - Drop the columns with missing values
LoanPrep = LoanPrep.dropna()


# Create Dummy variables - Not required in designer
LoanPrep = pd.get_dummies(LoanPrep, drop_first=True)


# Get the arguments from pipeline job
from argparse import ArgumentParser as AP

parser = AP()
parser.add_argument('--datafolder', type=str)
args = parser.parse_args()


# Create the folder if it does not exist
import os
os.makedirs(args.datafolder, exist_ok=True)

# Create the path
path = os.path.join(args.datafolder, 'defaults_prep.csv')

# Write the data preparation output as csv file
LoanPrep.to_csv(path, index=False)


# Log null values
for column in all_cols:
    new_run.log(column, dataNull[column])


# Complete the run
new_run.complete()
























