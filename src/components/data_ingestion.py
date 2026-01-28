import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass #this is used because it provides a decorator and functions for automatically 
        #adding generated special methods such as __init__() and __repr__() to user-defined classes.
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationonfig
from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import  ModelTrainerConfig



@dataclass
class DataIngestionconfig: #this helps in storing the file paths, creating a function so we can call it whenever needed
    train_data_path: str = os.path.join('artifacts', 'train.csv') #all the train data will be stored in artifact and named as train.csv
    test_data_path: str = os.path.join('artifacts', 'test.csv') #all the test data will be stored in artifact and named as test.csv
    raw_data_path: str = os.path.join('artifacts', 'data.csv') #all the raw data will be stored in artifact and named as data.csv, the raw data here is the original data

    #the data ingestion stores all the file paths for train, test and raw data so whenever new data comes in we can just call this
    #  function and it will store the data in the respective file paths.

class DataIngestion:
    def __init__(self):
      self.ingestion_config= DataIngestionconfig() #what does this line do? it
        # creates an instance of the DataIngestionconfig class and assigns it to the ingestion_config attribute of the DataIngestion class.
        # all the paths /config from the dataingestionconfig class are now stored in the ingestion_config attribute of the DataIngestion class.
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        
        try:
            df = pd.read_csv("notebook/data/stud.csv")  #THIS IS THE SOURCE,CAN CHANGE ONLY THIS ANYTIME A NEW DATA SOURCE(API,DB CONNECTS,CSV) COMES IN, THE REST OF THE CODE REMAINS SAME
            logging.info("Read the dataset as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True) #creating the artifact folder if not exists
            
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True) #storing the raw data in the raw data path
            
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42) #splitting the data into train and test set, 20% test size
            
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True) #storing the train data in the train data path
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True) #storing the test data in the test data path
            
            logging.info("Ingestion of the data is completed")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path    
            )
        
        except Exception as e:
            raise CustomException(e, sys)

if __name__=="__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation= DataTransformation()
    train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_data, test_data)

    model_trainer= ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))