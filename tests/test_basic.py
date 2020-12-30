
#########################################################################################
import os
import sys
import time
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from simple_store.simple_store import SimpleStore    
#########################################################################################

# (1) -> create instance using getInstance
db = SimpleStore.getInstance()

# (2) -> create instance using constructor
db = SimpleStore()

# (3) -> create key value pair where key is "string" and value is a json object(input provided as dict)
db.create(key="alphabets",value={"1":"a","2":"b","3":"c"},timeToLiveInSeconds=0)

# (4) -> create with time to live property
db.create(key="numbers",value={"1":"01","2":"01","3":"03"},timeToLiveInSeconds=30)

# (5) -> read
print(db.read(key="alphabets"))

# (6) -> delete
db.delete(key="numbers")

# (7) -> close instance
db.close()