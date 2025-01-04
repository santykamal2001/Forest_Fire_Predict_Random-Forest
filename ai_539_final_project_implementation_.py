# -*- coding: utf-8 -*-
"""AI 539 Final Project Implementation .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16UIgcV9gj162XbA78PAD66D4P3kXqLs0

Final Project Implementation

AI 539

Santhos Kamal Arumugam Balamurugan

03/18/2024

Reference: Chatgpt
"""

# Commented out IPython magic to ensure Python compatibility.
#load libararies
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
# %matplotlib inline
import seaborn as sns

#load datasets
data = pd.read_csv('/content/covtype.csv')
data.head()

#list of columns
print(data.columns)

#shape of data
data.shape

# Initialize an empty set to store unique values
unique_values = set()

# Iterate through each column in the dataset
for column in data.columns:
    # Extract unique values from the column and add them to the set
    unique_values.update(data[column].unique())

# Count the number of unique values (classes)
num_classes = len(unique_values)

print("Number of classes in the dataset:", num_classes)

data.describe()

#About Target/Cover_Type variable
data.Cover_Type.value_counts()

#count plot of target
sb.countplot(x='Cover_Type', data=data)
plt.show()

#Take some column
col = ['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology',
       'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
       'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
       'Horizontal_Distance_To_Fire_Points']

train = data[col]

#histogram
train.hist(figsize=(13, 11))
plt.show()

#Boxplot
plt.style.use('ggplot')
for i in col:
    plt.figure(figsize=(13, 7))
    plt.title(str(i) + " with " + str('Cover_Type'))
    sb.boxplot(x=data.Cover_Type, y=train[i])
    plt.show()

#Corralation
plt.figure(figsize=(12, 8))
corr = train.corr()
sb.heatmap(corr, annot=True)
plt.show()

"""**Random Forest Implementation and its accuracy**"""

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel

#separate features and target
feature = data.iloc[:, :54] #Features of data
y = data.iloc[:, 54]  #Target of data

# Features Reduction
ETC = ExtraTreesClassifier()
ETC = ETC.fit(feature, y)

model = SelectFromModel(ETC, prefit=True)
X = model.transform(feature) #new features

#shape of new feature
X.shape

#Split the data into test and train formate
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=10)

#Random Forest
from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier(n_estimators=100)

#fit
RFC.fit(X_train, y_train)

#prediction
y_pred = RFC.predict(X_test)

#score
print("Accuracy -- ", RFC.score(X_test, y_test)*100)

#confusion
cm = confusion_matrix(y_pred, y_test)
plt.figure(figsize=(10, 8))
sb.set(font_scale=1.2)
sb.heatmap(cm, annot=True, fmt='g')
plt.show()

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)

# R-squared Error
r_squared = r2_score(y_test, y_pred)
print("R-squared Error:", r_squared)

"""Strategy 1: **Resampling Technique**"""

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import RandomOverSampler

# Define resampling strategy
over_sampler = SMOTE(sampling_strategy=0.5)
under_sampler = RandomUnderSampler(sampling_strategy=0.8)

ros = RandomOverSampler()

# Define pipeline with resampling steps
pipeline = Pipeline([
    ('over', over_sampler),
    ('under', under_sampler)
])

# Apply resampling to training data
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)

from sklearn.ensemble import RandomForestClassifier

# Defining the classifier with adjusted class weights
RFC = RandomForestClassifier(n_estimators=100, class_weight='balanced')

# Train the classifier on the resampled training data
RFC.fit(X_train_resampled, y_train_resampled)

#Random Forest
from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier(n_estimators=100)

#fit
RFC.fit(X_train, y_train)

# Prediction Of RFC
y_pred = RFC.predict(X_test)

# Printing the accuracy Resampling Technique with RFC Test score
print("Accuracy -- ", RFC.score(X_test, y_test)*100)

# Imp confusion Matrix
cm = confusion_matrix(y_pred, y_test)
plt.figure(figsize=(10, 8))
sb.set(font_scale=1.2)
sb.heatmap(cm, annot=True, fmt='g')
plt.show()

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)

# R-squared Error
r_squared = r2_score(y_test, y_pred)
print("R-squared Error:", r_squared)

"""Strategy: 1 **Cost-Sensitive Learning**"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sb

# Defining the class weights for multi-class classification
class_weights = 'balanced'

# Initialize RandomForestClassifier with class weights
RFC_weighted = RandomForestClassifier(n_estimators=100, class_weight=class_weights)

try:
    # Fit the model
    RFC_weighted.fit(X_train, y_train)

    # Make predictions
    y_pred_weighted = RFC_weighted.predict(X_test)

    # Evaluate the model
    accuracy_weighted = RFC_weighted.score(X_test, y_test)
    print("Accuracy with class weights:", accuracy_weighted)

    # Confusion matrix
    cm_weighted = confusion_matrix(y_test, y_pred_weighted)
    plt.figure(figsize=(10, 8))
    sb.set(font_scale=1.2)
    sb.heatmap(cm_weighted, annot=True, fmt='g')
    plt.title("Confusion Matrix with Class Weights")
    plt.show()

except ValueError as e:
    print("Error occurred during fitting the model:", e)

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)

# R-squared Error
r_squared = r2_score(y_test, y_pred)
print("R-squared Error:", r_squared)

"""Strategy:2 **Interquartile Range (IQR)**"""

df1=data.select_dtypes(exclude=['object'])
for column in df1:
        plt.figure(figsize=(17,1))
        sns.boxplot(data=df1, x=column)

def treat_outliers(column):
    Q1 = column.quantile(0.25)
    Q3 = column.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return column.apply(lambda x: np.clip(x, lower_bound, upper_bound))
num_columns = data.select_dtypes(include=[np.number]).columns
data[num_columns] = data[num_columns].apply(treat_outliers)
data

df1 = data.select_dtypes(exclude=['object'])

# Plot boxplots for numerical columns
for column in df1:
    plt.figure(figsize=(17, 1))
    sns.boxplot(data=df1, x=column)
    plt.show()

#Random Forest
from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier(n_estimators=100)

#fit
RFC.fit(X_train, y_train)

#prediction
y_pred = RFC.predict(X_test)

#score
print("Accuracy -- ", RFC.score(X_test, y_test)*100)

#confusion
cm = confusion_matrix(y_pred, y_test)
plt.figure(figsize=(10, 8))
sb.set(font_scale=1.2)
sb.heatmap(cm, annot=True, fmt='g')
plt.show()

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)

# R-squared Error
r_squared = r2_score(y_test, y_pred)
print("R-squared Error:", r_squared)

"""Strategy 2: **Trimming**"""

import numpy as np

data = pd.read_csv('/content/covtype.csv')

# Define trimming thresholds (replace these with your desired thresholds)
lower_threshold = 1  # Lower threshold for trimming outliers
upper_threshold = 10  # Upper threshold for trimming outliers

# Trim outliers from the dataset
trimmed_data = data[(data >= lower_threshold) & (data <= upper_threshold)]

# Print the trimmed data
print("Trimmed Data:\n", trimmed_data)

#Random Forest
from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier(n_estimators=100)

#fit
RFC.fit(X_train, y_train)

#prediction
y_pred = RFC.predict(X_test)

#score
print("Accuracy -- ", RFC.score(X_test, y_test)*100)

#confusion
cm = confusion_matrix(y_pred, y_test)
plt.figure(figsize=(10, 8))
sb.set(font_scale=1.2)
sb.heatmap(cm, annot=True, fmt='g')
plt.show()

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)

# R-squared Error
r_squared = r2_score(y_test, y_pred)
print("R-squared Error:", r_squared)

"""Strategy:3 **Min -Max Scaling**"""

import numpy as np

# Define your dataset (replace this with your actual dataset)
data = pd.read_csv('/content/covtype.csv')
# Define Min-max scaling function
def min_max_scaling(data):
    # Calculate the minimum and maximum values for each feature
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)

    # Perform min-max scaling for each feature
    scaled_data = (data - min_vals) / (max_vals - min_vals)

    return scaled_data

# Apply Min-max scaling to your dataset
scaled_data = min_max_scaling(data)

# Print the scaled dataset
print("Scaled Data:\n", scaled_data)

#Random Forest
from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier(n_estimators=100)

#fit
RFC.fit(X_train, y_train)

#prediction
y_pred = RFC.predict(X_test)

#score
print("Accuracy -- ", RFC.score(X_test, y_test)*100)

#confusion
cm = confusion_matrix(y_pred, y_test)
plt.figure(figsize=(10, 8))
sb.set(font_scale=1.2)
sb.heatmap(cm, annot=True, fmt='g')
plt.show()

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)

# R-squared Error
r_squared = r2_score(y_test, y_pred)
print("R-squared Error:", r_squared)

"""Strategy:3 **Standardization**"""

from sklearn.preprocessing import StandardScaler

# Initialize the StandardScaler
scaler = StandardScaler()

# Define your dataset (replace this with your actual dataset)
data = pd.read_csv('/content/covtype.csv')

# Fit the scaler to your data and transform it
scaled_data = scaler.fit_transform(data)

# Print the scaled data
print("Scaled Data:\n", scaled_data)

#Random Forest
from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier(n_estimators=100)

#fit
RFC.fit(X_train, y_train)

#prediction
y_pred = RFC.predict(X_test)

#score
print("Accuracy -- ", RFC.score(X_test, y_test)*100)

#confusion
cm = confusion_matrix(y_pred, y_test)
plt.figure(figsize=(10, 8))
sb.set(font_scale=1.2)
sb.heatmap(cm, annot=True, fmt='g')
plt.show()

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mae)

# R-squared Error
r_squared = r2_score(y_test, y_pred)
print("R-squared Error:", r_squared)