
########################################################################
import os
import sys
import json
import enum
import logging
from pathlib import Path
from datetime import datetime
from filelock import Timeout, FileLock
import time
########################################################################


class LastOperation(enum.Enum):
    CREATE = 0
    READ = 1
    DELETE = 2
    NONE = 3


class SimpleStore:
    # singleton instance
    __simpleStore = None
   
    # default path to the store
    __path = ""
   
    # default file name of the store if one is not provided using setPath()
    __fileName = None
    
    # data loaded from json file
    __loadedData = None

    # records the last performed operation to avoid reloading the entire json
    __lastOperation = LastOperation.NONE

    # flags if a file is present or not
    __isFilePresent = False

    # constant string values
    __TIME_TO_LIVE_IN_SECONDS = "time-to-live-in-seconds"
    __TIME_STAMP = "time-stamp"
    __DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    # returns the instance if present or creates a new instance
    @staticmethod
    def getInstance():
        if(SimpleStore.__simpleStore == None):
            SimpleStore.__simpleStore = SimpleStore()
        return SimpleStore.__simpleStore

    # !!! prefer using getInstance() if need only one instance and to avoid duplication
    # constructors are to used to invoke multiple instances
    # but object state won't be saved across constructors and it becomes a mess with many constructors.
    def __init__(self):

        self.__fileName = "SimpleStore"
        self.__loadedData = {}
        self.__lastOperation = LastOperation.NONE
        self.__isFilePresent = False
        # gets the current platform at runtime
        platform = sys.platform
        # provides path for current directory
        basePath = str(os.getcwd())
        # provides path of home directory
        home = str(Path.home())

        # returns the path respective to the operating system
        if(platform == "linux" or platform == "linux2"):
            self.__path = basePath + "/{0}.json".format(self.__fileName)
        elif(platform == "win32" or platform == "cygwin" or platform == "msys"):
            self.__path = basePath + "\{0}.json".format(self.__fileName)
        elif(platform == "darwin"):
            self.__path = basePath + "/{0}.json".format(self.__fileName)
        else:
            self.__path = basePath + "/{0}.json".format(self.__fileName)
            logging.critical(
                msg="your platform is currently not supported, functions may not perform as intended")

    # check if the user provided path is valid
    def __isPath(self, path: str) -> bool:
        if os.access(path, os.R_OK):
            return True
        else:
            return False

    # enables user to set custom path to the data store
    # optionally the user can hide the created file using the hidden parameter
    def setPath(self, path: str = __path, fileName: str = __fileName, hidden: bool = False) -> None:
        if(path != None):
            if(self.__isPath(path)):
                if(hidden == True):
                    self.__path = path.strip() + "/.{0}.json".format(fileName)
                else:
                    self.__path = path.strip() + "/{0}.json".format(fileName)
                # finds if the file is already present
                isFile = os.path.isfile(self.__path)

                if(self.__isFilePresent == False and isFile == False):
                    self.__updateJson()
                    print("File created at: " + self.__path)
                    self.__isFilePresent = True
                    return
                self.__isFilePresent = True
            else:
                logging.error("Invalid path for store")

    # creates lock on the current file
    def __getLock(self):
        lockFilePath = self.__path + ".lock"
        lock = FileLock(lockFilePath, timeout=1)
        return lock

    # loads the json file as dictionary
    def __loadJson(self):
        try:
            # gets lock on the file for reading
            # if file is heldby another process for more than 10 seconds, it throws timeout exception
            with self.__getLock().acquire(timeout=10):
                with open(self.__path, 'r') as file:
                    self.__loadedData = json.load(file)
                    # time.sleep(12)
        except Timeout:
            logging.error(
                "the lock is held by another instance of this application")
        except Exception as exception:
            logging.error(exception)

    # writes back the updated data to the store
    def __updateJson(self):
        try:
            # gets lock on the file for writing
            # waits for 10 seconds if the file is held by another operation
            with self.__getLock().acquire(timeout=10):
                with open(self.__path, 'w') as jsonFile:
                    json.dump(self.__loadedData, jsonFile, indent=2)

        except Timeout:
            logging.error(
                "the lock is held by another instance of this application") 
        except Exception as exception:
            logging.error(exception)

    # create a new key-value pair and append it to the loaded dictionary
    def create(self, key: str, value: dict = {}, timeToLiveInSeconds: int = 0):

        # if the size of the value(json object or dict) is greater than 16KB, then it discards
        if((sys.getsizeof(value)/1024) > 16):
            logging.warning("Json object value size should be less than 16KB")
            return

        if(self.__isFilePresent == False and self.__isPath(self.__path) == False):
            self.__updateJson()
            print("File created at: " + self.__path)
            self.__isFilePresent = True
        try:
            # verifies that the file size of a single store won't exceed 1GB
            # combined size is file size added to the the size of current value of dict
            size = "{:.2f}".format(
                float(((os.path.getsize(self.__path) + sys.getsizeof(value)) / (1024 * 1024))))
            if float(size) >= 1024.00:
                logging.error("The file size exceeds 1GB")
                return
            # verifies that the key length won't exceed 32 characters
            if len(key) > 32:
                logging.warning(
                    "please enter a key which is less than 32 characters")
                return

            self.__loadJson()

            if key in self.__loadedData.keys():
                if(self.__isValueDestroyed(key) == False):
                    logging.error(
                        "The entered key is already present, trying using another key")
                    return
                else:
                    pass

            self.__loadedData[key] = value
            self.__loadedData[key][self.__TIME_TO_LIVE_IN_SECONDS] = timeToLiveInSeconds
            self.__loadedData[key][self.__TIME_STAMP] = self.__getCurrentTimeInString(
            )
            self.__updateJson()
            self.__lastOperation = LastOperation.CREATE

        except Exception as exception:
            print(exception)
            return

    # returns the json object or dict for the provided key if present
    # else throws exception and returns empty dict or json object
    def read(self, key: str) -> dict:
        try:
            if(self.__lastOperation == None):
                pass
            else:
                self.__loadJson()

            # checks whether the Time to Live property has beem expired or not
            if(self.__isValueDestroyed(key) == False):
                value = self.__loadedData[key]
                self.__lastOperation = LastOperation.READ
                return value
            else:
                print("The value has been destroyed as Time to Live Expired")
                return {}

        except Exception as exception:
            logging.error("Key not found in store")
            return {}

    # deletes the key value pair for the given key if present
    def delete(self, key: str):
        try:
            if(self.__lastOperation == LastOperation.READ):
                pass
            else:
                self.__loadJson()

            # checks whether the Time to Live property has been expired or not
            if(self.__isValueDestroyed(key) == True):
                logging.warning(
                    "The value has been already destroyed as Time to Live Expired")
                return
            else:
                del self.__loadedData[key]
                self.__updateJson()
                self.__lastOperation = LastOperation.DELETE
                return

        except Exception as exception:
            logging.error("Deletion failed. Key not found in store")
            return

    # returns string value
    def __getCurrentTimeInString(self):
        return datetime.now().strftime(self.__DATE_TIME_FORMAT)

    # returns datetime object
    def __getCurrentTime(self):
        return datetime.now().replace(microsecond=0)

    # checks "Time to Live" property and returns whether the object has been destroyed or not
    def __isValueDestroyed(self, key: str):
        try:
            currentTime = self.__getCurrentTime()
            # string object
            timeStampInString = self.__loadedData[key][self.__TIME_STAMP]
            # datetime object
            timeStamp = datetime.strptime(
                timeStampInString, self.__DATE_TIME_FORMAT)
            # time difference
            deltaTimeInSeconds = int((currentTime - timeStamp).total_seconds())
            timeToLive = self.__loadedData[key][self.__TIME_TO_LIVE_IN_SECONDS]

            # 0 is default and is not destroyed
            if(timeToLive == 0):
                return False
            elif(deltaTimeInSeconds >= timeToLive):
                del self.__loadedData[key]
                self.__updateJson()
                return True
            else:
                return False

        except Exception as exception:
            logging.error(exception + " failed to delete")
            return

    # destroys the current alive object and resets
    # use this before creating a new second or nth instance to avoid duplication
    def close(self):
        # !!! be careful, the current state of the object will be lost and
        # !!! when requested again using getInstance(),
        # !!! a new instance will be created
        # however the last state of the data store will be preserved
        if(self.__simpleStore != None):
            self.__simpleStore = None
            self.__path = ""
            self.__fileName = None
            self.__loadedData = None
            self.__isFilePresent = False
            self.__lastOperation = LastOperation.NONE
            logging.warning("object state destroyed")
