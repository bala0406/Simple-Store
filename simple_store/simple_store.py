
########################################################################
import os
import sys
import json
import enum
from pathlib import Path
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
    __fileName = "SimpleStore"
    __loadedData = {}
    # records the last performed operation
    __lastOperation = LastOperation.NONE

    # returns the instance if present or creates a new instance
    @staticmethod
    def getInstance():
        if(SimpleStore.__simpleStore == None):
            SimpleStore.__simpleStore = SimpleStore()
        return SimpleStore.__simpleStore

    def __init__(self):
        platform = sys.platform
        home = str(Path.home())

        # returns the path respective to the operating system
        if(platform == "linux" or platform == "linux2"):
            self.__path = home + "/{0}.json".format(self.__fileName)
        elif(platform == "win32" or platform == "cygwin" or platform == "msys"):
            self.__path = home + "\{0}.json".format(self.__fileName)
        elif(platform == "darwin"):
            self.__path = home + "/{0}.json".format(self.__fileName)
        else:
            print("your platform is currently not supported")

    # check if the user provided path is valid
    def __isPath(self, path: str) -> bool:
        if os.access(path, os.R_OK):
            return True
        else:
            return False

    # enables user to set custom path to the data store
    def setPath(self, path: str = __path, fileName: str = __fileName) -> None:
        if(path != None):
            if(self.__isPath(path)):
                self.__path = path + "/{0}.json".format(fileName)
                self.__updateJson()
            else:
                print("!!!Invalid path for store!!!")

    # loads the jsonfile as dictionary
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
    # it also verifies that the file size of a single store won't exceed 1GB
    def create(self, key: str, value: dict):
        try:
            size = "{:.2f}".format(
                float(os.path.getsize(self.__path) / (1024 * 1024)))
            if float(size) >= 1024.00:
                print("The file size exceeds 1GB")
                return
            if len(key) > 32:
                print("please enter a key which is less than 32 characters")
                return

            self.__loadJson()
            if key in self.__loadedData.keys():
                print("The entered key is already present, trying using another key")
                return

            self.__loadedData[key] = value
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

            value = self.__loadedData[key]
            self.__lastOperation = LastOperation.READ
            return value
        except Exception as exception:
            print(exception)
            return {}

    # deletes the key value pair for the given key if present
    def delete(self, key: str):
        try:
            if(self.__lastOperation == LastOperation.READ):
                pass
            else:
                self.__loadJson()

            if(self.__loadedData[key] == None):
                return

            del self.__loadedData[key]
            self.__updateJson()
            self.__lastOperation = LastOperation.DELETE
        except Exception as exception:
            print(exception)
            return
