#########################################################################################
import os
import sys
from pathlib import Path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from simple_store.simple_store import SimpleStore  
#########################################################################################

db = SimpleStore.getInstance()

# !!! NOTE - set path creates a file if one is not present at the given directory
#######################################################################################
# case - 1 ----------- omitting set path or empty set path - both produce same results
#######################################################################################
db.setPath()

############################################################################################################
# case - 2 ----------- set path with file name only - creates file with given name at default location(cwd)
############################################################################################################
db.setPath(fileName="my_store")

########################################################
# case - 3 ----------- set path with file name and path
########################################################
home = str(Path.home())
db.setPath(path=home,fileName="my_store")

#####################################################################################
# case - 2 ----------- set path with file name and path with option to hide the file
#####################################################################################
# !!! Currently hidden file only works on unix machines, 
# !!! the parameter isHidden will be ignored on windows if one is provided.
db.setPath(path="",fileName="my_store",isHidden=True)


db.close()