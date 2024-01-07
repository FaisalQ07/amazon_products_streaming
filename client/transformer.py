import os
import glob
import numpy as np
import pandas as pd
from numpy import add



for filepath in glob.iglob('../dataset/input/*.csv'):
    # read the files
    print(filepath)
    # extract the filename as tail 
    head, tail = os.path.split(filepath)
    filename = tail.split('.')[0]
    df = pd.read_csv(filepath)
    if filename == 'amazon_products_small':
        # add string date column for last day of the year
        print('---------------- adding date -------------------')
        df['date'] = '31/12/2023 00:00'

    # add a json column to the dataframe
    # splitlines will split the json into multiple rows not a single one
    df['json'] = df.to_json(orient='records', lines=True).splitlines()

    # take only the json column of the dataframe
    dfjson = df['json']
    print(dfjson)

    # print out the dataframe to a file in output folder of dataset
    # Note that the timestamp forward slash will be escaped to stay true to JSON schema
    np.savetxt(f'../dataset/output/{filename}.txt', dfjson.values, fmt='%s')
