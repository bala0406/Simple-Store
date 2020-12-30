
#########################################################################################
import os
import sys
import time
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from simple_store.simple_store import SimpleStore    
#########################################################################################

# db instance
db = SimpleStore.getInstance()
# or
db = SimpleStore()
# db = SimpleStore() can also be used for creating multiples instances within the same module

# the path will be set to default(current working directory) path if one is not provided
db.setPath(path="", fileName="my_store", isHidden=False)

##############################################################################
# case - 1 --------- inserting a dict value with key which is already present
##############################################################################
db.create(key="animal", value={"1": "elephant",
                               "2": "lion"}, timeToLiveInSeconds=0)
db.create(key="animal", value={"1": "tiger",
                               "2": "leopard"}, timeToLiveInSeconds=0)

############################################################
# case - 2 --------- checking the cap size of 16KB on value
############################################################
dummyDict = {}
for i in range(700):
    dummyDict[str(i)] = str(i)
db.create(key="animal", value=dummyDict, timeToLiveInSeconds=0)


db.close()

