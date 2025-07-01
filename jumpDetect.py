import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# This script reads a CSV file containing exchange rate data, and will detect the jumps
# We start by importing the necessary libraries and reading the data.

zarData = pd.read_csv('C:\HistoricalRateDetail.csv')

print(zarData.head())

# We have imported the South African Rand (ZAR) to Dollar exchange rate 
#Checking for missing values in the dataset
print(zarData.isnull().sum())


logretZarData = np.log(zarData['Value'] / zarData['Value'].shift(1))
logretZarData.pop(0)  # Remove the first NaN value after shift
# We calculate the log returns for the ZAR exchange rate data.
print("Log Returns for ZAR Data:", logretZarData.head())

k=20
bipVar = np.zeros(len(logretZarData)-2-k)
realVar = np.zeros(len(logretZarData)-2-k)
for i in range(len(logretZarData)-2-k):
    # Calculate the bipower variation for each window of size k
    # The bipower variation is a measure of volatility based on the absolute differences
    # between consecutive prices.
    for j in range(k):
        realVar[i] = (logretZarData[j+i+2] - logretZarData[j+i+1]) * (logretZarData[j+i+2] - logretZarData[j+i+1])
        bipVar[i] += abs(logretZarData[j+i+2] - logretZarData[j+i+1]) * abs(logretZarData[j+i+3] - logretZarData[j+i+2])
   

print("Bipower Variation:", bipVar)
print("Realised Variance:",realVar)
# We have calculated the realised bipower variation for the ZAR exchange rate data.
# This will help us identify significant jumps in the exchange rate by estimating the
#  instantaneous volatility.

diffSqZarData = (realVar - bipVar) * (realVar - bipVar)
print("Difference Squared:", diffSqZarData)

zarDataDates = (zarData['Date'][3+k:]).values

# We have calculated the squared difference between the realised variance and the bipower variation.
# This will help us identify significant jumps in the exchange rate.
# The following plot will display the squared differences over time and the peaks in the data indicate
# potential jumps in the exchange rate.
plt.plot(zarDataDates,diffSqZarData)
plt.show()