'''
when multiple process try to perform read or write operations, the data in the store becomes inconsistent.
# so a lock has to be made on the store while performing operations.
# hence others process have to wait in a queue while other process is performing operations on the store.

'''

'''
----------------------- to produce the above circumstance follow the below steps ---------------------------
1. open two terminals with path set to the project folder.

2. uncomment the 156th line in the simple_store.py module(time.sleep) in simple_store package to
simulate the waiting process with a timeout of 10 seconds.

3. now try to run any two programs from the two terminals simultaniously with create,read or delete
operation which requires the access to the file.

4. the file which gets access to the file first locks the file, performs the operation and sleeps for 10
seconds for the sake of simulating this thread safe process.

5. the following process waits for 10 seconds for the lock to be released and quits after 10 seconds if
the lock is not released.
-------------------------------------------------------------------------------------------------------------
'''