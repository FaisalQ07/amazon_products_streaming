import os
import numpy as np
import pandas as pd
from numpy import add
import glob


for filepath in glob.iglob('../dataset/input/*.csv'):
    # read the files
    print(filepath)
    # extract the filename as tail 
    head, tail = os.path.split(filepath)
    filename = tail.split('.')[0]
    df = pd.read_csv(filepath)

    # add a json column to the dataframe
    # splitlines will split the json into multiple rows not a single one
    df['json'] = df.to_json(orient='records', lines=True).splitlines()

    # take only the json column of the dataframe
    dfjson = df['json']
    print(dfjson)

    # print out the dataframe to a file in output folder of dataset
    # Note that the timestamp forward slash will be escaped to stay true to JSON schema
    np.savetxt(f'../dataset/output/{filename}.txt', dfjson.values, fmt='%s')
