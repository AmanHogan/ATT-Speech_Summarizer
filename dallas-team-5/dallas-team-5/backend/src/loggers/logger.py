from datetime import datetime
import os.path
import sys
sys.dont_write_bytecode = True


# INIT CONSTANTS
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(SCRIPT_DIR, '../../db/logs/logFile.txt')


####################################################################
#   function - logs text data into a log file
#   params - data - a string that contains data to be printed in log
#   returns - None
#####################################################################
def logData(data):

    if not (os.path.isfile(LOG_FILE_PATH)):
       fp = open(LOG_FILE_PATH, "w")
       fp.close()

    else:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        fp = open(LOG_FILE_PATH, "a+")
        fp.write(f"{timestamp} :: {data}\n")
        fp.close()