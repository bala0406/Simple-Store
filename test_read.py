from simple_store.simple_store import SimpleStore


db = SimpleStore.getInstance()
db.setPath("/home/bala/FreshworksAssignment","dummy")
print(db.read("animal"))