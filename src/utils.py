import os
import sys

import numpy as np
import pandas as pd 
import dill
from sklearn.metrics import r2_score
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import GridSearchCV

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

def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    """
    This function evaluates multiple models and returns their R2 scores
    """
    try:
        report = {}

        for model_name, model in models.items():

            if model_name not in params:
                 raise CustomException(f"Params not found for model: {model_name}", sys)
            if model_name == "CatBoost Regressor":
                model.fit(X_train, y_train)
                y_test_pred = model.predict(X_test)
                report[model_name] = r2_score(y_test, y_test_pred)
                continue

            para = params.get(model_name, {})
           

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)
            
            report[model_name] = test_model_score


        return report

    except Exception as e:
        raise CustomException(e, sys)

