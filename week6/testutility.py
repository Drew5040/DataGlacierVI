import os
import time
import logging
import subprocess
import yaml
import datetime
import re
import string
import random
import psutil
import gc
import graphviz
import objgraph
import pandas as pd
import dask.dataframe as dd


# Reads the YAML configuration file
def read_config_file(filepath):
    
    # Open specified filepath
    with open(filepath, 'r') as datacreek:
        # Try-Catch for YAMLError
        try:
            return yaml.safe_load(datacreek)
        except yaml.YAMLError as exc:
            # Logging library error sent to 'stdout'
            logging.error(exc)
            
# Specify characters to remove using regex
def replacer(string, char):
    
    # Regex pattern for 2 or more instances
    pattern = char + '{2,}'
    
    # Sub function to replace specified char
    string = re.sub(pattern, char, string)
    
    # Returns the string with replaced char
    return string

def col_header_val(df, table_config):
    '''replace whitespaces in the column
       standardize column names
    '''
    # Convert all strings to lowercase
    df.columns = df.columns.str.lower()
    print('1', df.columns, '\n')
    # Replace all whitespce at the start of column names
    df.columns = df.columns.str.replace('[^\w]', '_', regex=True)
    print('2', df.columns, '\n')
    # Removes underscores from beginning & end of column names
    df.columns = list(map(lambda x: x.strip('_'), list(df.columns)))
    print('3', df.columns, '\n')
    # Replaces 2 or more consecutive underscores with a single underscore
    df.columns = list(map(lambda x: replacer(x, '_'), list(df.columns)))
    print('4', df.columns, '\n')
    # Converts expected col_names for 'table_config' to ensure case insensitivity during comaparison
    expected_col = list(map(lambda x: x.lower(), table_config['columns']))
    print('5', expected_col, '\n')
  
    # Converts all column names in df once again. Ensures case insensitivity when comparing with expected col_names
    df.columns = list(map(lambda x: x.lower(), list(df.columns)))
    print('6', df.columns, '\n')
    


    # Sort the DataFrame by multiple columns
    df = df[table_config['columns']]
    print('7', df.head(), '\n')
    

    # Check if the sorted column names in df match the sorted expected column names
    if list(expected_col) == list(df.columns):
        print('Column name and column length validation passed')
        return True

    if len(df.columns) == len(expected_col) and list(expected_col) == list(df.columns):
        print('column namd and column length validation passed')
        return True
    
    # If the above is false, then we check what the differences are between df.col and exp_col and print them
    else:
        print('column name and column length validation failed')
        # Uses set operations for taking the difference between df.col and exp_col
        mismatched_columns_file = list(set(df.columns).difference(expected_col))
        print('The following YAML columns are not in the YAML file', mismatched_columns_file )
        # Uses set operations to check diff between exp_col and df_col
        missing_yaml_file = list(set(expected_col).difference(df.columns))
        print('The following YAML columns are not in the uploaded file', missing_yaml_file)
        
        logging.info(f'df columns: {df.columns}')
        logging.info(f'expected columns: {expected_col}')
        return False
