from flask import Flask
from flask import request
from flask_apscheduler import APScheduler
import csv
from flask import g


app = Flask(__name__)

class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='do_job_1', seconds=1, misfire_grace_time=900)
def periodic_task():
    pass

@app.route('/checkfile')
def checkfile():
  file = request.args.get('file', default = "", type = str)
  with open('completed.txt') as myfile:
     if file in myfile.read():
         return "-1"
  return "1"

@app.route('/addqueue')
def addqueue():
    file = request.args.get('file', default = "", type = str)
    
    my_list = []
    with open('queue.txt', newline='') as f:
        reader = csv.reader(f)
        my_list = list(reader)
    
    my_list[0].append(file)

    with open('queue.txt', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(my_list[0])

    return "0"

@app.route('/removequeue')
def removequeue():
    my_list = []
    with open('queue.txt', newline='') as f:
        reader = csv.reader(f)
        my_list = list(reader)
    
    my_list[0].pop(1)

    with open('queue.txt', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(my_list[0])

    return "0"

@app.route('/checkqueue')
def checkqueue():
    my_list = []
    with open('queue.txt', newline='') as f:
        reader = csv.reader(f)
        my_list = list(reader)
    return str(my_list[0])

@app.route('/getready')
def readready():
    if_ready = getattr(g, '_ready', None)
    if (if_ready):
        setattr(g, '_ready', False)
    return str(if_ready)

@app.route('/setready')
def setready():
    setattr(g, '_ready', True)
    return ""



if __name__ == '__main__':
    app.run(debug=True)