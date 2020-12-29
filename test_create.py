from simple_store.simple_store import SimpleStore


db = SimpleStore.getInstance()
db.setPath("/home/bala/FreshworksAssignment","dummy")


db.create("animal",{"1":"elephant","2" : "bird"},500)

# db.create("animal",{"1":"elephant","2" : "lion"})
# print(db.read("animal"))

