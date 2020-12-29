from simple_store.simple_store import SimpleStore


db = SimpleStore()
db.setPath("/home/bala/FreshworksAssignment","dummy")


db.create("animal",{"1":"elephant","2" : "bird"})

# db.create("animal",{"1":"elephant","2" : "lion"})
# print(db.read("animal"))

