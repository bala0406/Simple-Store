
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
# case - 1 --------- reading a data with an invalid key
########################################################
db.create(key="wild-animals", value={
          "1": "elephant", "2": "lion"}, timeToLiveInSeconds=10)

print(db.read("non-wild-animals"))

#########################################################################
# case - 2 --------- reading a value after time to live property expired
#########################################################################
db.create(key="non-wild-animals", value={"1": "cat",
                                         "2": "dog"}, timeToLiveInSeconds=5)
time.sleep(6)
print(db.read("non-wild-animals"))


db.close()