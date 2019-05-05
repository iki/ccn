#!/usr/bin/env python3.6
#-*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from numpy import loadtxt
from libPlotting import *



def FilterDatabase(SPPdb, query, FieldIndex):
    # Version Python2
    SPPdbFiltered = np.array(SPPdb[SPPdb[:,FieldIndex]!=query,:]) 
    # Version Python3 (without for loop)
    #SPPdbFiltered = list(filter(SPPdb[:,FieldIndex],query)) #Error: TypeError: 'numpy.int64' object is not iterable
    ## Version Python3 (with loops)
    #SPPdbFiltered=[]
    #for line in SPPdb:
        #if(FieldIndex!=line[FieldIndex]):
            #SPPdbFiltered.append(line)
    return SPPdbFiltered

def FilterDatabaseEqual(SPPdb, query, FieldIndex):
    # Version Python2
    SPPdbFiltered = np.array(SPPdb[SPPdb[:,FieldIndex]==query,:]) 
    # Version Python3 (without for loop)
    #SPPdbFiltered = list(filter(SPPdb[:,FieldIndex],query)) #Error: TypeError: 'numpy.int64' object is not iterable
    ## Version Python3 (with loops)
    #SPPdbFiltered=[]
    #for line in SPPdb:
        #if(FieldIndex!=line[FieldIndex]):
            #SPPdbFiltered.append(line)
    return SPPdbFiltered

## Plots the input file "e2a9b544-0a44-4ab1-b0c4-78079eb0d800"
def plotSimplifiedData(): #{{{
    # Input
    MoleculeNumber=0

    # Dictionnaries
    molecules={0: "PM10", 1: "PM2_5"}

    Fields={"year": 1, "month": 2, "day": 3, "concentration": 4, "species": 5, "latitude": 6, "longitude": 7, "time": 8}

    InputFile="e2a9b544-0a44-4ab1-b0c4-78079eb0d800.csv"

    # Converting the XML dataset into 1 CSV file.
    CSV_subset = np.loadtxt(InputFile, dtype='str', delimiter=",", skiprows=1)
    print("Number of samples: ", np.shape(CSV_subset))
    # Filter the molecular to visualize

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
    #timecapture   =CSV_subset[:,Fields["time"]]

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

    # Converting time
    #instant_str=year+"-"+Months_num+"-"+day+"T"+timecapture
    #instant_str=np.concatenate((year, Months_num),axis=1)
    #instants=np.datetime64(instant_str)

    #print(year)
    #print(Months_num)

    #print(np.shape(year))

    year_t          = year.astype(int)
    months_t        = Months_num.astype(int)
    day_t           = day.astype(int)
    concentration_t = concentration.astype(np.float128)
    latitude_t      = latitude.astype(np.float128)
    longitude_t     = longitude.astype(np.float128)
    #time_t          = timecapture.astype(int) ## BUG : neglected

    print(longitude_t)

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
    del latitude, longitude, concentration
    del latitude_t, longitude_t, concentration_t

    query = order[0] #WARNING: we select the first timeslice for now
    NewTable_t=np.transpose(NewTable)

    #TimeSlice=NewTable_t #NOTE: this just avoids no database scenario
    TimeSlice=FilterDatabase(NewTable_t, query, 0) #4 columns with only one 1 timeslice
    print("Number of samples in the timeslice: ", np.shape(TimeSlice))

    print(TimeSlice)

    #order           = TimeSlice[:, 0]
    latitude        = TimeSlice[:, 1] 
    longitude       = TimeSlice[:, 2]
    concentration   = TimeSlice[:, 3]
    #print(latitude)
    #exit()
    SortedTable     = TimeSlice[np.lexsort((concentration, longitude, latitude))]
    #order_s         = SortedTable[:, 0]
    longitude_s     = SortedTable[:, 2] #X
    latitude_s      = SortedTable[:, 1] #Y
    concentration_s = SortedTable[:, 3] #Z

    print("Shape of longitudinal SET: ", np.shape(list(set(np.float128(longitude_s)))))
    print("Shape of latitude SET: ", np.shape(list(set(np.float128(latitude_s)))))

    NumberOfPoints=np.size(longitude_s)

    #WARNING: plotting the initial dataset is failing! 
    #We need a bijective function for X or Y axis. Here data are 5x5. 
    X = longitude_s
    Y = latitude_s
    DataOfInterest = concentration_s

    print("Shape of X SET: ", np.shape(list(set(np.float128(X)))))
    print("Shape of Y SET: ", np.shape(list(set(np.float128(Y)))))

    print(Y)

    #### Test for the plotting
    print("Random points: ", NumberOfPoints)
    del Y
    RegularMesh=np.linspace(0,10,NumberOfPoints) 
    RandomMesh=np.random.rand(NumberOfPoints)
    Y=RandomMesh
    #Y=latitude_s #np.random.rand(NumberOfPoints) #np.linspace(1, 10, NumberOfPoints)
    #DataOfInterest=concentration_s

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
#}}}

## Plots the input file "merge.csv"
#def plotCompleteDataset(): #{{{
# Input
MoleculeNumber=1

Molecules={1: "NO2", 2: "O3", 3: "PM10", 4: "PM10_24", 5: "PM2_5", 6: "SO2"}

# Dictionnaries
Fields={"latitude": 10, "longitude": 11, "NO2": 13, "O3": 14, "PM10": 16, "PM10_24": 17, 
        "PM2_5": 18, "SO2": 19, "timestamp": 20}

InputFile="merge.csv"

# Converting the XML dataset into 1 CSV file.
CSV = np.genfromtxt(InputFile, dtype='str', delimiter=",", skip_header=1, filling_values=0)

#CSV_subset = CSV_subset[0:1, :]

print("Total number of samples: ", np.shape(CSV))
# Filter the molecular to visualize

#query = Fields[Molecules[MoleculeNumber]]
query=''
CSV_subset = FilterDatabase(CSV, query, Fields[Molecules[MoleculeNumber]])
print("Cleaning the database from empty samples of ", Molecules[MoleculeNumber])
print("Number of samples: ", np.shape(CSV_subset)) #works

# We have to clean the data right here
#CSV_subset = [[]]
#for row in CSV:
    #if(row[Fields[Molecules[MoleculeNumber]]]!=''):
        #CSV_subset.append(row)
    ##else: 
        ##print(row)
#print()
concentration=CSV_subset[:,Fields[Molecules[MoleculeNumber]]]
latitude     =CSV_subset[:,Fields["latitude"]]
longitude    =CSV_subset[:,Fields["longitude"]]
timecapture  =CSV_subset[:,Fields["timestamp"]]

# Converting time
stamps=pd.to_datetime(timecapture)
timestamps_epoch = (stamps - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
#print(timestamps_epoch)

# Managing concentrations
print("Molecule: ", Molecules[MoleculeNumber])
#print("Example : ", CSV_subset[:,Fields[Molecules[MoleculeNumber]]])

## Tables are ndarrays for now... Not practical. 
time_t      = timestamps_epoch.astype(int)
longitude_t = longitude.astype(float) #OK
latitude_t  = latitude.astype(float) #OK
#print(concentration)

concentration_filtered = []
try:
    concentration_t = concentration.astype(float) #BUG: some samples actually have no measurements for all species
except:
    line_id=0
    for line in concentration:
        try: 
            line.astype(float)
            concentration_filtered.append(line)
        except:
            print("Error line ", line_id)
            print(line)
        line_id+=1
        

NewTable_formatted = np.transpose(np.array([time_t, longitude_t, latitude_t, concentration_t]))
print("Simplified table, made of floats?")
#print(NewTable_formatted)
### All samples not necessarily have a value. We need to select line where sample has been taken. 
#concentration_filtered = []
#time_filtered          = []
#longitude_filtered     = []
#latitude_filtered      = []

#print(concentration.astype(float))

#NewTable = np.concatenate(time_t, longitude_t) #, latitude), concentration)
## Projecting to simple types
#concentration_l = concentration.tolist()
#latitude_l      = latitude.tolist()
#longitude_l     = longitude.tolist()
#timecapture_l   = timestamps_epoch.tolist()
#print(concentration_l)

#concentration_t = np.array(concentration_l)
#latitude_t      = np.array(latitude_l)
#longitude_t     = np.array(longitude_l)
#time_t          = np.array(timestamps_epoch)

#print(concentration_t.astype(float))

print(time_t)

# Sorting the subset as function of day and time. 
timeslices=np.array(list(set(time_t))) #keeps only unique values for timesteps
print("Number of time slices: ", len(timeslices))
print("Time slices set:", timeslices)


#NewTable=np.transpose(np.array([time_t, latitude_t, longitude_t, concentration_t]))

print("Simplified table shape: ", np.shape(NewTable_formatted))

del latitude, longitude, concentration
del latitude_t, longitude_t, concentration_t

#NewTable_t = np.float(NewTable_t) .astype(float)
print(NewTable_formatted)
for slice_id in np.arange(0,len(timeslices)):
    query = timeslices[slice_id] #WARNING: we select the first timeslice for now
    #TimeSlice=NewTable_t #NOTE: this just avoids no database scenario
    print("Timestep: ", query)
    TimeSlice=FilterDatabaseEqual(NewTable_formatted, query, 0) #4 columns with only one 1 timeslice
    print("Number of samples in the timeslice: ", np.shape(TimeSlice))

    print(TimeSlice)

    #order           = TimeSlice[:, 0]
    latitude        = TimeSlice[:, 1] 
    longitude       = TimeSlice[:, 2]
    concentration   = TimeSlice[:, 3]
    #print(latitude)
    #exit()
    SortedTable     = TimeSlice[np.lexsort((concentration, longitude, latitude))]
    #order_s         = SortedTable[:, 0]
    longitude_s     = SortedTable[:, 2] #X
    latitude_s      = SortedTable[:, 1] #Y
    concentration_s = SortedTable[:, 3] #Z

    print("Shape of longitudinal SET: ", np.shape(list(set(np.float128(longitude_s)))))
    print("Shape of latitude SET: ", np.shape(list(set(np.float128(latitude_s)))))

    NumberOfPoints=np.size(longitude_s)

    #WARNING: plotting the initial dataset is failing! 
    #We need a bijective function for X or Y axis. Here data are 5x5. 
    #For this reason, I slightly correct the initial data with invisible noise. 
    Y = longitude_s #+ 1E-5*np.random.rand(NumberOfPoints)
    X = latitude_s #+ 1E-5*np.random.rand(NumberOfPoints)
    DataOfInterest = concentration_s

    print("Shape of X SET: ", np.shape(list(set(np.float128(X)))))
    print("Shape of Y SET: ", np.shape(list(set(np.float128(Y)))))

    #print(X)

    #### Test for the plotting
    #print("Random points: ", NumberOfPoints)
    #NumberOfPoints=23
    #RegularMesh=np.linspace(0,10,NumberOfPoints) #np.random.rand(NumberOfPoints)
    #X=RegularMesh
    #Y=latitude_s #np.random.rand(NumberOfPoints) #np.linspace(1, 10, NumberOfPoints)
    #DataOfInterest=concentration_s

    #fig=plt.figure()
    print("X: min, max: ", np.min(X), np.max(X))
    print("Y: min, max: ", np.min(Y), np.max(Y))
    print("Data: min, max: ", np.min(DataOfInterest), np.max(DataOfInterest))

    # Isolate each timestep and plot into a separate PNG file
    print("Dimension X: ", np.shape(X))
    print("Dimension Y: ", np.shape(Y))
    print("Dimension Z: ", np.shape(DataOfInterest))

    #plot2dScatteredPoints(X, Y, DataOfInterest, "Pollution", "Pollution.png", True) #WORKS
    filename="Pollution-"+str(Molecules[MoleculeNumber])+"-"+str(query)+".png"
    plot2dHeatMap(X, Y, DataOfInterest, "Pollution", "Pollution.png", True) #WORKS
#}}}
    #plotSimplifiedData()
    #plotCompleteDataset()
