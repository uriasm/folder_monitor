## Folder monitor
Monitor the files and folders changes inside a given path, store the metadata information of the changes in a firebase database and send a message to a guest with the information to retrieve the metadata from firebase. Then the guest will retrieve the information and store it.


## Prerequisites

```bash
python 3
```
**Install dependencies**

Install all dependencies that are required for the project by running:

```bash
pip3 install -r requirements.txt
```

## How to use
```bash
pyton3 main.py <FOLDER-PATH-TO-MONITOR>
```
**Result**

- The entire flow of the program will be displayed on the console.
- The resulting json file is located at ./src/events.json