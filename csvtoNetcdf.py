from netCDF4 import Dataset
import numpy as np
import pandas as pd
import numpy as np


# CSV Format is Label followed by 10MFCCs.
# After reading the csv file, I exclude the labels and create 
# an array of just the 10 MFCCs. Those 10 mfccs are converted to 
# NETCDF form

rawDump = np.array(pd.read_csv("/Users/kirit/BtechProject/Analysis/DataDumps/dataDump.csv", header=None))

data = rawDump[:, 1:]

# Create and open the netcdf dataset
root_grp = Dataset('menData.nc', 'w', format='NETCDF4')

# Various attributes can be given to the group.
# Description, institution etc can be added.
root_grp.description = 'MFCC data'

# Since all my MFCCs are of the same dimension (i.e. same number of MFCCs for the 0th, 1st, 2nd and so on)
# I create only one dimension which will be used to describe all my mfccs.
root_grp.createDimension("MFCC", data.shape[0])

# variables
# Since I have 10 mfccs, I create 10 variable. 
# Each variable has the name dimensions (MFCC) that I created above. Dimension must be passed as a tuple.
# The data type given in double (d)
# The name of each variable is mfcc0, mfcc1, mfcc2 and so on
mfccvariables = []
for i in range(data.shape[1]):
	mfccvariables.append(root_grp.createVariable('mfcc' + str(i), 'd', ('MFCC',)))

# data
# The data for each variable is passed in this loop
for i in range(len(mfccvariables)):
	mfccvariables[i][:] = data[:, i]

# Close the netcdf dataset
root_grp.close()