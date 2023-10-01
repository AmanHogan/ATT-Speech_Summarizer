import matplotlib
matplotlib.use('Agg')
import torch
import numpy
import pandas
import torch.nn as nn
import torch.optim as optim
import torch
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import src.loggers.logger as logger
import re
import sys
sys.dont_write_bytecode = True


GENERATIONS = 400

#############################################################
#   function - Trains an ML model using MLR on a csv db
#   returns - None
#   params - None
##############################################################
def initializeModel():
    logger.logData('Training ML Model...')
    # Class function - formats structure of tensors and data
    class Data(Dataset):
        
        # Constructor
        def __init__(self):

            self.x = trainData
            w = torch.zeros(10,27)
            b = 1
            func = torch.mm(self.x, w) + b    
            self.y = trainLabels
            self.len = self.x.shape[0]

        def __getitem__(self, idx):          
            return self.x[idx], self.y[idx]
        
        def __len__(self):
            return self.len

    # Class function - creating a  Multiple Linear Regression Model using input data
    class MultipleLinearRegression(torch.nn.Module):
        
        def __init__(self, input_dim, output_dim):
            super(MultipleLinearRegression, self).__init__()
            self.linear = torch.nn.Linear(input_dim, output_dim)
        
        # returns prediction values
        def forward(self, x):
            y_pred = self.linear(x)
            return y_pred


    # Define Features and Labels
    featureFields = ['ConnectionType','Provider','EmployeeCount','Bandwidth','MajorIssue','DataCap','DeviceAge','RouterLocation','NetworkLatency','Usage']
    labelFields = ['ProviderIssue','SignalIssue','LegacyIssue','LatencyIssue','SpywareIssue','ConnectionTypeIssue','BandwidthIssue']

    # Get data from dbs
    trainData = torch.tensor((pandas.read_csv('./db/training/training-data.csv', nrows=27, sep=',', usecols=featureFields).astype('int32')).values, dtype=torch.float32)
    trainLabels = torch.tensor((pandas.read_csv('./db/training/training-data.csv', nrows=27, sep=',', usecols=labelFields)).astype('int32').values, dtype=torch.float32)
    clientData = torch.tensor((pandas.read_csv('./db/training/client-data.csv', nrows=1, sep=',', usecols=featureFields).astype('int32')).values, dtype=torch.float32)

    # Initialize Model, optimizer, criterion, and train_loader
    data_set = Data()
    MLR_model = MultipleLinearRegression(10,7)
    optimizer = torch.optim.SGD(MLR_model.parameters(), lr=0.1)
    criterion = torch.nn.MSELoss()
    train_loader = DataLoader(dataset=data_set, batch_size=2)

    # Train the model over succesive generations
    losses = []
    for epoch in range(GENERATIONS):
        for x,y in train_loader:
            y_pred = MLR_model(x)
            loss = criterion(y_pred, y)
            losses.append(loss.item())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    print(f"losses = {losses[GENERATIONS - 1]}")
    logger.logData('Machine Learning Model was succesfully trained')

    # Plot the loss function
    plt.plot(losses)
    plt.xlabel("no. of iterations")
    plt.ylabel("total loss")
    plt.savefig("./src/ml/loss.png")
    logger.logData(f'Model Started with a loss of {losses[0]} and ended with a loss of {losses[GENERATIONS - 1]}')
    predictClientSolution(clientData, MLR_model)

#############################################################
#   function - runs client csv data against model and logs the 
#   predicted values.
#   params - 
#       - clientData - tensor of client data 
#       - MLR_model - Trained Model
#   returns - None
##############################################################
def predictClientSolution(clientData, MLR_model):
    fp = open("./db/predictions/client-predictions.txt", "w")
    fh = open("./db/predictions/client-recommendation-db.csv", "w")
    
    fh.write("ProviderIssue,SignalIssue,LegacyIssue,LatencyIssue,SpywareIssue,ConnectionTypeIssue,BandwidthIssue\n")

    clientPredictionTensor = MLR_model(clientData)
    clientPredictionList = clientPredictionTensor.detach().numpy().flatten().tolist()
    
    logger.logData(f'Client predictions: {clientPredictionList}')
    clientPredictionDictionary = {
        "ProviderIssue": round(clientPredictionList[0]),
        "SignalIssue": round(clientPredictionList[1]),
        "LegacyIssue": round(clientPredictionList[2]),
        "LatencyIssue": round(clientPredictionList[3]),
        "SpywareIssue": round(clientPredictionList[4]),
        "ConnectionTypeIssue": round(clientPredictionList[5]),
        "BandwidthIssue": round(clientPredictionList[6]),
    }

    index = 0
    for key, value in clientPredictionDictionary.items():
        if value == 0:
            fh.write("0,")
        else:
            fh.write("1,")

        fp.write(f"A {100 if round(abs(clientPredictionList[index]) * 100) >= 100 else round(abs(clientPredictionList[index]) * 100)}% chance {key} is the problem\n")    
        index = index + 1

    fp.close()
    fh.close()

    logger.logData('Client solutions successfully predicted')
    print('Client solutions successfully predicted')

    reccomendSolutions(clientPredictionList, index)


####################################################################################
#   function - Recommends solutions based on the confidence percentage values of the
#   found issues.
#   params  - clientPredictionList - confidence % val of each issue
#           - index - number of predictions
#   returns - None
####################################################################################
def reccomendSolutions(clientPredictionList, index):
    
    index = 0
    perecentageIssue = []
    for i in range(len(clientPredictionList)):
        perecentageIssue.append(100 if round(abs(clientPredictionList[index]) * 100) >= 100 else round(abs(clientPredictionList[index]) * 100))
        index = index + 1
    print(f'List of percentages: {perecentageIssue}')

    dictionary = {
        "ProviderIssue": 
        [
            "AT&T Dedicated Internet up to 1 Tbps speed", 
            "AT&T Business Fiber 5 GIG speed",
            "AT&T Business Fiber 2 GIG speed",
            "AT&T Business Fiber 500 MB speed"
        ],
        "SignalIssue":  ["a Wi-fi extender from the current models: AirTies 4971 and AirTies 4921"],
        "LegacyIssue" : 
        [
            "new Wi-FI gateways from the current models: BGW320, BG210, PACE 5268",
            "some new Cat6 Ethernet cables" 
        ],
        "LatencyIssue" : ["AT&T Business Fiber 5 GIG speed"],
        "LatencyIssue" : [ "AT&T Internet Security Suite - Powered by McAfee"],
        "ConnectionTypeIssue" : [ "AT&T Business Fiber 5 GIG speed"],
        "BandwidthIssue" : [ "AT&T Business Fiber 5 GIG speed"]               
    }

    listOfRecommendations = []

    # Recommend Solution based on % value
    if perecentageIssue[0] >= 90:
        listOfRecommendations.append(dictionary["ProviderIssue"][0])
    elif perecentageIssue[0] >= 80 and perecentageIssue[0] < 90:
        listOfRecommendations.append(dictionary["ProviderIssue"][1])
    elif perecentageIssue[0] >= 70 and perecentageIssue[0] < 80:
        listOfRecommendations.append(dictionary["ProviderIssue"][2])
    elif perecentageIssue[0] >= 60 and perecentageIssue[0] < 70:
        listOfRecommendations.append(dictionary["ProviderIssue"][3])

    if perecentageIssue[1] >= 50:
        listOfRecommendations.append(dictionary["SignalIssue"][0])

    if perecentageIssue[2] >= 80:
        listOfRecommendations.append(dictionary["LegacyIssue"][0])
    elif perecentageIssue[2] >= 50 and perecentageIssue[2] < 80:
        listOfRecommendations.append(dictionary["LegacyIssue"][1])

    if perecentageIssue[3] >= 50:
        listOfRecommendations.append(dictionary["LatencyIssue"][0])

    if perecentageIssue[4] >= 50:
        listOfRecommendations.append(dictionary["LatencyIssue"][0])
    
    if perecentageIssue[5] >= 50:
        listOfRecommendations.append(dictionary["ConnectionTypeIssue"][0])

    if perecentageIssue[5] >= 80:
        listOfRecommendations.append(dictionary["BandwidthIssue"][0])

    listOfRecommendationsTemp = getUniqueItems(listOfRecommendations)
    numOfRecommendations = len(listOfRecommendationsTemp)

    if numOfRecommendations == 0:
        listOfRecommendations.append("AT&T Business Fiber 5 GIG speed")

    if numOfRecommendations > 1:
        lastRecommendation = listOfRecommendations[numOfRecommendations - 1]
        listOfRecommendations.remove(lastRecommendation)
        listOfRecommendations.append("and")
        listOfRecommendations.append(lastRecommendation)

    ########### PARSE RECOMMENDATIONS #######################################################
    listOfRecommendations = getUniqueItems(listOfRecommendations)
    listOfRecommendations = str(listOfRecommendations).replace("'", "").replace("[]", "")
    listOfRecommendations = re.sub(r"[\[\]]", "", listOfRecommendations)
    
    if numOfRecommendations > 1:
        listOfRecommendations = listOfRecommendations.replace("and,", "and")

    fr = open("../uploads/client-recommendation.txt", "w")

    listOfRecommendations = "We recommend " + listOfRecommendations + "."
    fr.write(listOfRecommendations)
    fr.close()
    logger.logData(f'Client Recommendations: {listOfRecommendations}')

# Makes a unique ordered list
def getUniqueItems(iterable):
    result = []
    for item in iterable:
        if item not in result:
            result.append(item)
    return result
