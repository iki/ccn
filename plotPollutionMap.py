#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-

import numpy as np
from numpy import loadtxt
from libPlotting import *

# Input
MoleculeNumber=1

# Dictionnaries
molecules={0: "PM10", 1: "PM2_5"}

Fields={"year": 1, "month": 2, "day": 3, "concentration": 4, "species": 5, "latitude": 6, "longitude": 7, "time": 8}

InputFile="e2a9b544-0a44-4ab1-b0c4-78079eb0d800.csv"

# Converting the XML dataset into 1 CSV file.
CSV_subset = np.loadtxt(InputFile, dtype='str', delimiter=",", skiprows=1)
print("Number of samples: ", np.shape(CSV_subset))
# Filter the molecular to visualize

def FilterDatabase(SPPdb, query, FieldIndex):
  SPPdbFiltered = np.array(SPPdb[SPPdb[:,FieldIndex]==query,:]) #uses a table of booleans to select
  return SPPdbFiltered

query = molecules[MoleculeNumber]

CSV_subset = FilterDatabase(CSV_subset, query, Fields["species"])
print("Selecting subset for molecule ", molecules[MoleculeNumber])
print("Number of samples: ", np.shape(CSV_subset))

year          =CSV_subset[:,Fields["year"]]
months_str    =CSV_subset[:,Fields["month"]]
day           =CSV_subset[:,Fields["day"]]
concentration =CSV_subset[:,Fields["concentration"]]
species       =CSV_subset[:,Fields["species"]]
latitude      =CSV_subset[:,Fields["latitude"]]
longitude     =CSV_subset[:,Fields["longitude"]]
time          =CSV_subset[:,Fields["time"]]

print("Possible molecules: ", set(species))

Months_CZ={"duben": 4, "květen": 5}
    #"leden": 01,
    #"\C3 BAnor": 02, 
        #"březen": 03, 
        #"červen": 06, 
        #"červenec": 07, 
        #"srpen": 08, 
        #"září": 09, 
        #"říjen": 10, 
        #"listopad": 11, 
        #"prosinec": 12 

## Convert the month name to number
i=0

Months_num = np.zeros(np.size(months_str))
for months in months_str:
    Months_num[i] = Months_CZ[months]
    i+=1
del i

#print(year)
#print(Months_num)

#print(np.shape(year))

year_t          = year.astype(int)
months_t        = Months_num.astype(int)
day_t           = day.astype(int)
concentration_t = concentration.astype(np.float128)
latitude_t      = latitude.astype(np.float128)
longitude_t     = longitude.astype(np.float128)
#print(day_t)
#year_t       = np.ndarray(1, dtype=int, year)
#Months_num = np.ndarray(Months_num)
#day_t        = np.ndarray(1, dtype=int)

# Sorting the subset as function of day and time. 
# Maybe convert everything in hours? 

# We have to select only one set of TIME

# TODO: warning, this does not account for 30/31-days calendar months. Use a library for this. 
order=np.add(np.add(np.multiply(np.add(year_t,0),365), np.multiply(months_t, 30)), day_t)

timeslices=set(order) #keeps only unique entries for timesteps
NewTable     =np.array([order, latitude_t, longitude_t, concentration_t])
print("Simplified table shape: ", np.shape(NewTable))

query = order[0] #WARNING: we select the first timeslice for now
NewTable_t=np.transpose(NewTable)

TimeSlice=NewTable_t #NOTE: this just avoids no database scenario
TimeSlice=FilterDatabase(NewTable_t, query, 0) #4 columns with only one 1 timeslice

print("Number of samples in the timeslice: ", np.shape(TimeSlice))
order           = TimeSlice[:, 0]
latitude        = TimeSlice[:, 1]
longitude       = TimeSlice[:, 2]
concentration   = TimeSlice[:, 3]
#print(latitude)
#exit()
SortedTable     = TimeSlice[np.lexsort((concentration, latitude, longitude, order))]
order_s         = SortedTable[:, 0]
longitude_s     = SortedTable[:, 2] #X
latitude_s      = SortedTable[:, 1] #Y
concentration_s = SortedTable[:, 3]

#print(latitude_s)

#exit()

X = longitude
Y = latitude
DataOfInterest = concentration

#### Test
#X=np.array([0, 1, 2, 3])
#Y=np.multiply(X,-1)
#DataOfInterest=np.power(X,2)


#fig=plt.figure()
print("X: min, max: ", np.min(X), np.max(X))
print("Y: min, max: ", np.min(Y), np.max(Y))
print("Data: min, max: ", np.min(DataOfInterest), np.max(DataOfInterest))

# Isolate each timestep and plot into a separate PNG file
print("Dimension X: ", np.shape(X))
print("Dimension Y: ", np.shape(Y))
print("Dimension Z: ", np.shape(DataOfInterest))


plot2dScatteredPoints(X, Y, DataOfInterest, "Pollution", "Pollution.png", True) #WORKS

plot2dHeatMap(X, Y, DataOfInterest, "Pollution", "Pollution.png", True) #FAILS
