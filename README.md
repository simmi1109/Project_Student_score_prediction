🎓 Student Math Score Prediction
📌 Overview -

This project predicts a student’s Math Score using:

Reading Score
Writing Score
Gender
Race/Ethnicity
Parental Level of Education
Lunch Type

Test Preparation Course - 

It is a regression problem solved using multiple ML models with automated model selection.

🚀 Approach -

Performed EDA and preprocessing
Applied encoding for categorical features
Trained multiple regression models:
Linear Regression
Decision Tree
Random Forest
Gradient Boosting
AdaBoost
KNN
XGBoost
CatBoost
Hyperparameter tuning performed
Best model selected using R² score
Model and preprocessor saved in artifacts/

🧠 Pipeline Design -

Modular training & prediction pipeline
Custom logging and exception handling
Serialized model using pickle
Clean project structure for production readiness

🌐 Deployment - 

Built a Flask web application
Created HTML frontend for user input
Integrated trained model for real-time prediction
End-to-end ML deployment from training → inference