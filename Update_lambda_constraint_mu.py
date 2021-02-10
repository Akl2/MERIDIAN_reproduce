#!/usr/bin/env python
# coding: utf-8


import csv
import numpy as np 
import random
import time
# sve_ivp
from scipy.integrate import solve_ivp
from collections import defaultdict
# import concurrent.futures 
import os
# with open('names.csv')
import pandas as pd



## Load Lambda old. 
## Load data 
## get constraints data 
## get new lambda 
## save new lambda 



outputfolder = '/blue/pdixit/hodaakl/output/MaxEnt_0210/Run1/'


def calculate_constraints(data):
    """ inputs (data) with shape = (ncells, nConditions) : ncells would represent the number of MCMC samples taken"""
    mu = np.mean(data, axis = 0 ) # means along the column, to get the mean over all the cells
    # s =  np.mean(data**2, axis = 0 ) # means along the column, to get the mean over all the cells
    return mu
# 
# 
def update_lambda(Error, old_lambda, alpha = 0.01 ):
    alpha_array = alpha*np.ones(24)
    Lambda = old_lambda.copy() + alpha_array*(Error)
    return Lambda




lambda_path = outputfolder +'Lambdas.csv'
lambdadf = pd.read_csv(lambda_path, sep = ',', header = None)
Lambda_np = lambdadf.to_numpy()
iterationp1, _ = Lambda_np.shape
iteration = iterationp1 -1


filename_abund = outputfolder + f'SS_data_{iteration}.csv'
df = pd.read_csv(filename_abund, sep = ',') 


data = df.to_numpy()


Constraints = np.load('/blue/pdixit/hodaakl/Data/SingleCellData/Constraints_mu_akt21_egfr3.npy')
# Constraints = Constraints[:24]
Preds = calculate_constraints(data)
# Preds = np.append(mu_sim, s_sim)
Error = Preds - Constraints 
print('avg abs error of iteration ' + str(iteration) + '=' + str(round(np.mean(abs(Error)),3)))
# rel_err = Error/Constraints
file_name_error = outputfolder+ 'Errors.csv'
file_name_lambda =outputfolder+ 'Lambdas.csv'
# file_name_avg_abs_error =outputfolder+ 'Avg_abs_error.csv'

Old_Lambda = Lambda_np[-1,:]
# avgabserr = np.mean(abs(Error))
Lambda = update_lambda(Error = Error, old_lambda= Old_Lambda, alpha = 0.05/500) 
Lambda= Lambda.tolist()
Error = Error.tolist()



#################################################### Storing the error 
if os.path.exists(file_name_error): 
    with open(file_name_error, 'a') as add_file_error:
        csv_adder_error = csv.writer(add_file_error, delimiter = ',')
        csv_adder_error.writerow(Error)
        add_file_error.flush()
else:
    with open(file_name_error, 'w') as new_file_error:

        csv_writer_error = csv.writer(new_file_error, delimiter = ',')
#         csv_writer_pars.writerow(Par_fieldnames)
        csv_writer_error.writerow(Error)
        new_file_error.flush()
    
#################################################### Storing the Lambda  

if os.path.exists(file_name_lambda): 
    with open(file_name_lambda, 'a') as add_file_lambda:
        csv_adder_lambda = csv.writer(add_file_lambda, delimiter = ',')
        csv_adder_lambda.writerow(Lambda)
        add_file_lambda.flush()
else:
    print('trouble loading file')