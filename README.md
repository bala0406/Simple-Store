<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/bala0406/Simple-Store">
    <img src="logo.png" alt="Logo" width="96" height="96">
  </a>

  <h3 align="center">Simple Store</h3>

  <p align="center">
    A File based key-value Data Store
    <br />
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#features">Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

A File based key-value data store that can be used in your project to store data in key value pairs in `json file` in your local machine. The `Simple Store` is very light weight and can be used in a small or medium scale projects. The `Time to live` property is a great feature if you don't want the data to be stored permanently. It destroys the data automatically after the time has expired. The read and write operations are also `thread-safe`, so you don't need to worry about concurrent access to the store. If you're on an UNIX machine you can also able to `hide` your data store file. The size of the value that can be stored for a single key is capped at `16KB` for faster read and write. The file size is also capped at `1GB` to keep the process light. So plan accordingly.

### Built With
* [Python :rocket:](https://www.python.org/)

### Features
* File stored as json :tada:
* Time to Live :hourglass:
* Thread safe :muscle:
* File hiding :closed_lock_with_key: (works only on UNIX based Operating Systems)
* Runs on all major Operating Systems :computer: (mac, linux, windows)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/bala0406/Simple-Store.git
   ```
2. Install required packages in `requirements.txt`
   ```sh
   pip3 install -r requirements.txt
   ```

<!-- USAGE EXAMPLES -->
## Usage
1. Copy the `simple_store` package folder into your project.

2. Import the `SimpleStore` class into your python file and get an instance of the store.
    ```sh        

    from simple_store.simple_store import SimpleStore 

    # if you need only one instance, you can prefer using the getInstance() static method in the class
    db = SimpleStore.getInstance()

    # if you need more than one instance, you can go with normal object creation for the class
    db = SimpleStore()
    ```

3. You can optionally set custom directory, file name and hidden property to the data store file. It's completely fine to skip this step and the data store file will be created in your `current project directory` with a default file name `SimpleStore` with file hiding defaulted to `False`.
   ```sh
   # isHidden property is defaulted to false
   db.setPath(path="your path goes here", fileName="enter your fileName here")

   # create file with default path 
   db.setPath(fileName="enter your fileName here") 

   # create file with default file name
   db.setPath(path="your path goes here")

   # hide file
   # NOTE: the file hiding only works on UNIX machines and isHidden parameter will be ignored on windows.
   db.setPath(path="your path goes here", fileName="enter your fileName here", isHidden=True) 
   ``` 

4. Create data in store.
   ```sh 
    # the key is a string and value is a dict object that will be converted to json
    dummyDict = {} # your dict
    db.create(key="enter your key here", value=dummyDict)

    # the default time to live value is 0 which means None.
    # create data with time to live property
    db.create(key="enter your key here", value=dummyDict,timeToLiveInSeconds=10)
   ```

5. Read data from store.
   ```sh 
    # it takes key as the parameter and returns the dict object converted from json object
    result = db.read(key="enter your key here")
    print(result)
   ```
5. Delete data in store.
   ```sh 
    # it takes key as the parameter 
    db.delete(key="enter your key here")
   ```

    `
    NOTE : The value will be mostly operated on dict object for wider compatibility within python and will be converted to json on storing the value to the data store. The operation is vice versa for reading.`

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [filelock :lock:](https://pypi.org/project/filelock/)


