import requests
import patoolib
import os
import time
count = 0
#os.mkdir("./upload")
while(True):
    if_ready = requests.get('http://52.14.130.151/getready')
    if (if_ready.text == "ready"):
        if not os.path.exists("./" + str(count)):
            os.mkdir("./"+ str(count))
            os.mkdir("./"+ str(count) +"/current")
            os.mkdir("./"+ str(count) +"/extraction")
        patoolib.extract_archive("upload/file.zip", outdir="./"+ str(count) +"/extraction", interactive=False)
        os.remove("upload/file.zip")
        requests.get("http://52.14.130.151/removequeue")
        txt = os.system("bash job.sh " + str(count))
        count += 1
    time.sleep(0.5)
