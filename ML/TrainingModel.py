import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os
from joblib import dump

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
    return x, y, Numeric

def Standard_Scaler(x, y):
    scaler = StandardScaler()
    x_scaler = scaler.fit_transform(x)
    x_train, x_test, y_train, y_test = train_test_split(x_scaler, y, test_size=0.3, random_state=42)
    feature_names = x.columns
    return x_train, x_test, y_train, y_test, scaler, feature_names


def Random_Forest(x_train, x_test, y_train, y_test, scaler, Numeric, feature_names):
    model = RandomForestClassifier(n_estimators=50)
    model.fit(x_train, y_train)
    prediction = model.predict(x_test)
    accuracy = accuracy_score(y_test, prediction)
    print('Random Forest: Accuracy: {:.2f}'.format(accuracy))
    print(classification_report(y_test, prediction))
    cm = confusion_matrix(y_test, prediction)
    plt.figure(figsize=(12, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=Numeric.classes_, yticklabels=Numeric.classes_)
    plt.title('Random Forest - Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.tight_layout()
    plt.show()
    dump(model, "model.pkl")
    dump(scaler, "scaler.pkl")
    dump(Numeric, "encoder.pkl")
    dump(feature_names, "features.pkl")
    
    print("Saved: model.pkl, scaler.pkl, encoder.pkl, features.pkl")

if __name__ == '__main__':
    data = loading_dataset()
    x, y, Numeric = new_dataset(data)
    x_train, x_test, y_train, y_test, scaler, feature_names = Standard_Scaler(x, y)
    Random_Forest(x_train, x_test, y_train, y_test, scaler, Numeric, feature_names)