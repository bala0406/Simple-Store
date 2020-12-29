
########################################################################
import os
import sys
import json
import enum
from pathlib import Path
from datetime import datetime
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
    __fileName = "SimpleStore"

    # loaded data from json file using __loadJson()
    __loadedData = {}

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

    def __init__(self):
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
            print("your platform is currently not supported")

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
                    print("File created at:" + self.__path)
                    self.__isFilePresent = True
                    return
                self.__isFilePresent = True
            else:
                print("!!!Invalid path for store!!!")

    # loads the json file as dictionary
    def __loadJson(self):
        try:
            with open(self.__path, 'r') as file:
                self.__loadedData = json.load(file)
        except Exception as exception:
            print(exception)
            return

    # writes back the updated data to the store
    def __updateJson(self):
        try:
            with open(self.__path, 'w') as jsonFile:
                json.dump(self.__loadedData, jsonFile, indent=2)
        except Exception as exception:
            print(exception)
            return

    # create a new key-value pair and append it to the loaded dictionary
    def create(self, key: str, value: dict = {}, timeToLiveInSeconds: int = 0):
        # if the size of the value(json object or dict) is greater than 16KB, then it discards
        if((sys.getsizeof(value)/1024) > 16):
            print("Json object value size should be less than 16KB")
            return

        if(self.__isFilePresent == False and self.__isPath(self.__path) == False):
            self.__updateJson()
            print("File created at:" + self.__path)
            self.__isFilePresent = True
        try:
            # verifies that the file size of a single store won't exceed 1GB
            # combined size is file size added to the the size of current value of dict
            size = "{:.2f}".format(
                float(((os.path.getsize(self.__path) + sys.getsizeof(value)) / (1024 * 1024))))
            if float(size) >= 1024.00:
                print("The file size exceeds 1GB")
                return
            # verifies that the key length won't exceed 32 characters
            if len(key) > 32:
                print("please enter a key which is less than 32 characters")
                return

            self.__loadJson()

            if key in self.__loadedData.keys():
                print("The entered key is already present, trying using another key")
                return

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
                return
        except Exception as exception:
            print("Key not found in store")
            return {}

    # deletes the key value pair for the given key if present
    def delete(self, key: str):
        try:
            if(self.__lastOperation == LastOperation.READ):
                pass
            else:
                self.__loadJson()

            # if(self.__loadedData[key] == None):
            #     return

            # checks whether the Time to Live property has been expired or not
            if(self.__isValueDestroyed(key) == True):
                print("The value has been already destroyed as Time to Live Expired")
                return
            else:
                del self.__loadedData[key]
                self.__updateJson()
                self.__lastOperation = LastOperation.DELETE
                return
        except Exception as exception:
            print("Deletion failed. Key not found in store")
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
            print(exception)
            return False

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
            self.__fileName = "SimpleStore"
            self.__loadedData = {}
            self.__isFilePresent = False
            self.__lastOperation = LastOperation.NONE
