import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import time
import os

def loading_dataset():
    folder_path = r"C:\Users\Acer\Desktop\CYSE689\TrafficLabelling"
    all_files = []
    for cvs in os.listdir(folder_path):
        if cvs.endswith('.csv'):
            file = os.path.join(folder_path,cvs)
            all_files.append(file)
    return all_files

#Defining new dataset
#Converting into numeric
def new_dataset(data):
    new_data = []
    for file in data:
        try:
            infor = pd.read_csv(file, encoding = 'ISO-8859-1')
            new_data.append(infor)
        except:
            print('Error reading {}, trying a different encoding.'.format(file))
            infor = pd.read_csv(file, encoding = 'latin1')
            new_data.append(infor)
    all_data = pd.concat(new_data,ignore_index = True)
    all_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    all_data.dropna(inplace = True)
    all_data.columns = all_data.columns.str.strip()
    x = all_data.drop(columns = ['Flow ID','Source IP','Destination IP','Timestamp','Label'])
    Numeric = LabelEncoder()
    y = Numeric.fit_transform(all_data['Label'])
    return x, y

def Standard_Scaler(x,y):
    scaler = StandardScaler()
    x_scaler = scaler.fit_transform(x)
    x_train,x_test,y_train,y_test = train_test_split(x_scaler,y,test_size=0.3,random_state=42)
    return x_train, x_test, y_train, y_test

def KNN(x_train, x_test, y_train, y_test):
    start = time.time()
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(x_train, y_train)
    prediction = model.predict(x_test)
    end = time.time()
    accuracy = accuracy_score(y_test, prediction)
    print('KNN: Accuracy: {:.2f} | Time: {:.2f} ms'.format(accuracy, (end - start)*1000))
    print(classification_report(y_test, prediction))
    scores = cross_val_score(model, np.concatenate([x_train, x_test]), np.concatenate([y_train, y_test]), cv=5)
    print("Cross-validation scores:", scores)
    print("Mean accuracy: {:.2f}, Std Dev: {:.2f}".format(scores.mean(), scores.std()))

def KNN_CV(x, y):
    start = time.time()
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(x, y)
    scores = cross_val_score(model, x, y, cv=5)
    predictions = cross_val_predict(model, x, y, cv=5)
    end = time.time()
    print(f"\nKNN Cross Validation")
    print("Cross-validation scores:", scores)
    print(f"Accuracy: {scores.mean():.4f} | Time: {(end - start) * 1000:.2f} ms")
    print("Classification Report:")
    print(classification_report(y, predictions))

if __name__ == '__main__':
    data = loading_dataset()
    x, y = new_dataset(data)
    x_train, x_test, y_train, y_test = Standard_Scaler(x,y)
    KNN(x_train, x_test, y_train, y_test)
    KNN_CV(x, y)