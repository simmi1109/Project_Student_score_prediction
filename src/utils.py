import os
import sys

import numpy as np
import pandas as pd 
import dill

from src.exception import CustomException

def save_object(file_path, obj):
    '''
    This function is used to save a python object as a binary file using dill
    #so basically storing the pkl file in hard disk
    '''
    try:
        dir_path = os.path.dirname(file_path) #getting the directory path from the file path
        os.makedirs(dir_path, exist_ok=True) #creating the directory if not exists

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj) #dumping the object into the file

    except Exception as e:
        raise CustomException(e, sys)