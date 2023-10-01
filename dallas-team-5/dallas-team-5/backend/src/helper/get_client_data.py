import random
import src.loggers.logger as logger
import os
import sys
sys.dont_write_bytecode = True

# INIT CONSTANTS
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_DATA_PATH = os.path.join(SCRIPT_DIR,"../../db/training/client-data.csv")

#####################################################
#   function - Initialize hard coded client data and 
#   write to a csv file
#   params - None
#   returns - None
######################################################
def initClientData():
    try:
        f = open(CLIENT_DATA_PATH, "w")
        f.write("ConnectionType,Provider,EmployeeCount,Bandwidth,MajorIssue,DataCap,DeviceAge,RouterLocation,NetworkLatency,Usage\n")
        f.write("4,1,1,2,1,1,3,2,2,1\n")
        f.close()
        logger.logData(f'Client Data was loaded')
        print('Client Data was loaded successfully')
    except:
        logger.logData(f'Client Data could not be loaded')
        print('Client Data was loaded successfully')
