
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
# db = SimpleStore() can also be used for creating multiples instances within the same module

# the path will be set to default(current working directory) path if one is not provided
db.setPath(path="", fileName="my_store", isHidden=False)

########################################################
# case - 1 --------- deleting a data with an invalid key
########################################################
db.create(key="planes", value={
          "1": "boeing-747", "2": "boeing-737"}, timeToLiveInSeconds=10)

db.delete("aircrafts")

#############################################################################
# case - 2 --------- deleting a data after its time to live property expired
#############################################################################
db.create(key="jet", value={"1": "private-jet",
                            "2": "hired-jet"}, timeToLiveInSeconds=5)
time.sleep(6)
db.delete("jet")


db.close()