import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer #for handling missing values

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object #for saving the pkl file

@dataclass #this helps us to create a class which will store the file paths, we dont have to write init method again and again
class DataTransformationconfig:
    preprocessor_obj_file_path= os.path.join('artifacts','preprocessor.pkl') #storing the preprocessor object in artifacts folder as preprocessor.pkl

class DataTransformation:
    def __init__(self):
        self.data_transformation_config= DataTransformationconfig() #storing the config file path in the data_transformation_config attribute

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            logging.info("Data Transformation initiated")
            #numerical columns
            num_features = ['reading_score', 'writing_score']
            #categorical columns
            cat_features = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            #numerical pipeline to handle missing values and scaling
            num_pipeline= Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy='median')), #to handl outliers we are using median
                       ("scaler", StandardScaler())
                       ] #scaling the numerical features so that they have mean 0 and variance 1
            )

            cat_pipeline= Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy='most_frequent')), #handling missing values by most frequent value
                       ("one_hot_encoder", OneHotEncoder(handle_unknown="ignore")), #one hot encoding the categorical features
                       ("scaler", StandardScaler(with_mean=False))] #scaling the categorical features
            )
            logging.info("Numerical and categorical pipelines created")
            #combining both numerical and categorical pipelines

            
            preprocessor= ColumnTransformer(
                 transformers=[
                    ("num_pipeline", num_pipeline, num_features),  #applying num_pipeline to num_features
                    ("cat_pipeline", cat_pipeline, cat_features)   #applying cat_pipeline to cat_features
                ]
            )
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):

        try:
            #reading train and test data
            train_df= pd.read_csv(train_path) # this data comes from data ingestion component(check artifacts folder)
            test_df= pd.read_csv(test_path) # this data comes from data ingestion component but we didnt import it here, we are just reading the csv files directly from the paths which is passed to this function
            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessor object")
            preprocessor_obj= self.get_data_transformer_object()

            target_column_name= 'math_score'
            num_columns = ['reading_score', 'writing_score']

            input_feature_train_df = train_df.drop(columns=[target_column_name]) #dropping the target column from train data
            target_feature_train_df= train_df[target_column_name] #storing only the target column in a separate variable

            input_feature_test_df= test_df.drop(columns=[target_column_name]) #dropping the target column from test data
            target_feature_test_df= test_df[target_column_name] #storing only the target column in a separate variable
            
            logging.info("Applying preprocessing object on training and testing datasets.")

            #transforming using preprocessor object
            input_feature_train_arr= preprocessor_obj.fit_transform(input_feature_train_df) #like x_train.fit_transform()
            input_feature_test_arr= preprocessor_obj.transform(input_feature_test_df) #like x_test.transform()

            #usually the x and y are kept separate but here we are combining them for ease of use in model training
             #refer the below code for better understanding
            #combining input features and target column back together
            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df).reshape(-1, 1)] 
            #what is np.c_? it is used to concatenate two arrays along the second axis, here we are concatenating input features and target column to create a single array for train data
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df).reshape(-1, 1)]


            logging.info("Data Transformation Completed")
            
            save_object(
                file_path= self.data_transformation_config.preprocessor_obj_file_path,
                obj= preprocessor_obj
            ) #this is done to save the preprocessor object for future use in model training and deployment

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
        

        #alternatively, the initiate_data_transformation method can be written as below:
        """def initiate_data_transformation(self, train_path, test_path):
          #Apply preprocessing to train and test datasets.#
          try: # read train and test data 
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path) 
            logging.info("Train and test data read successfully") 
            target_column_name = 'math_score'
              # split features and target
              X_train = train_df.drop(columns=[target_column_name]) 
              y_train = train_df[target_column_name] 
              X_test = test_df.drop(columns=[target_column_name]) 
              y_test = test_df[target_column_name] 

              # get preprocessor 
              preprocessor = self.get_data_transformer_object() 
              logging.info("Applying preprocessing on train and test data") 

              # transform features 
              X_train_transformed = preprocessor.fit_transform(X_train) 
              X_test_transformed = preprocessor.transform(X_test) 
              logging.info("Data transformation completed") 
              return ( X_train_transformed, X_test_transformed, 
                y_train.to_numpy(), y_test.to_numpy(), 
                self.config.preprocessor_obj_file_path ) 
              
              
            except Exception as e: raise CustomException(e, sys)"""
        
        