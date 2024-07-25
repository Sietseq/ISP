from flask import Flask
from flask import request
import csv
from flask import g


app = Flask(__name__)

app.config['ready'] = "notready" # Global variable for Siku to know if it can start extracting the file. 

# Not used at the moment but may be used for a history of files. 
@app.route('/checkfile')
def checkfile():
  file = request.args.get('file', default = "", type = str)
  with open('completed.txt') as myfile:
     if file in myfile.read():
         return "-1"
  return "1"

# Add file to the queue of files to be uploaded. 
@app.route('/addqueue')
def addqueue():
    file = request.args.get('file', default = "", type = str)

    # Open file
    my_list = []
    with open('queue.txt', newline='') as f:
        reader = csv.reader(f)
        my_list = list(reader)

    # Add new entry
    my_list[0].append(file)

    # Write file
    with open('queue.txt', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(my_list[0])

    return "0"

# Pop the last processed file from queue 
@app.route('/removequeue')
def removequeue():
    # Read file
    my_list = []
    with open('queue.txt', newline='') as f:
        reader = csv.reader(f)
        my_list = list(reader)

    # Remove entry
    my_list[0].pop(1)

    # Write file
    with open('queue.txt', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(my_list[0])

    return "0"

# Returns the current queue 
@app.route('/checkqueue')
def checkqueue():
    my_list = []
    with open('queue.txt', newline='') as f:
        reader = csv.reader(f)
        my_list = list(reader)
    return str(my_list[0])

# Returns the current ready state if ready send it but make it not ready after. 
@app.route('/getready')
def readready():
    if_ready = app.config['ready']
    if (if_ready == 'ready'):
        app.config['ready'] = 'notready'
    return if_ready

# Set ready to true
@app.route('/setready')
def setready():
    app.config['ready'] = 'ready'
    return ""

# Home page
@app.route('/')
def main():
    return "hello world"



if __name__ == '__main__':
    app.run(debug=True)
