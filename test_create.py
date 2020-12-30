from simple_store.simple_store import SimpleStore


db = SimpleStore()

db.setPath("D:\\",fileName="bala",isHidden=True)


db.create("animal", {"1": "elephant", "2": "lion"})
# print(db.read("animal"))
