import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

# Define the deep learning model for multi-class classification
# No sigmoid for CrossEntropy
class Detection(nn.Module):
    def __init__(self, input_size, d1, d2, num_classes):
        super(Detection, self).__init__()
        self.fc1 = nn.Linear(input_size, d1)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(d1, d2)
        self.relu2 = nn.ReLU()
        self.output = nn.Linear(d2, num_classes)  

    def forward(self, x):
        x = self.relu1(self.fc1(x))
        x = self.relu2(self.fc2(x))
        return self.output(x)  

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
    return x, y, len(np.unique(y))  # Return number of classes

# Scale and split
def Standard_Scaler(x, y):
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    return train_test_split(x_scaled, y, test_size=0.3, random_state=42)

# Convert to PyTorch tensors
def Convert_PyTorch(x_train, x_test, y_train, y_test):
    return (
        torch.tensor(x_train, dtype=torch.float32),
        torch.tensor(y_train, dtype=torch.long),
        torch.tensor(x_test, dtype=torch.float32),
        torch.tensor(y_test, dtype=torch.long),
    )

# Train the model
def training_model(model, x_train_tensor, y_train_tensor, optimizer, loss_fn, epochs=100, batch_size=32):
    dataset = TensorDataset(x_train_tensor, y_train_tensor)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    for epoch in range(epochs):
        for batch_x, batch_y in loader:
            optimizer.zero_grad()
            output = model(batch_x)
            loss = loss_fn(output, batch_y)
            loss.backward()
            optimizer.step()
        if epoch % 10 == 0:
            print(f"Epoch {epoch} - Loss: {loss.item():.4f}")
    return model

# Evaluate the model
def evaluation(model, x_test_tensor, y_test_tensor):
    model.eval()
    with torch.no_grad():
        output = model(x_test_tensor)
        _, predictions = torch.max(output, 1)
        accuracy = (predictions == y_test_tensor).sum().item() / y_test_tensor.size(0)
        print(f"\nAccuracy: {accuracy:.4f}")
        print("Confusion Matrix:")
        print(confusion_matrix(y_test_tensor, predictions))
        print("Classification Report:")
        print(classification_report(y_test_tensor, predictions))

# === Run the full process ===
if __name__ == '__main__':
    files = loading_dataset()
    x, y, num_classes = new_dataset(files)
    input_size = x.shape[1]

    model = Detection(input_size, 128, 64, num_classes)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    x_train, x_test, y_train, y_test = Standard_Scaler(x, y)
    x_train_tensor, y_train_tensor, x_test_tensor, y_test_tensor = Convert_PyTorch(x_train, x_test, y_train, y_test)
    trained_model = training_model(model, x_train_tensor, y_train_tensor, optimizer, loss_fn)
    evaluation(trained_model, x_test_tensor, y_test_tensor)