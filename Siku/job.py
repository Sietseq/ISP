import requests
import patoolib
import os
import time
count = 0
while(True):
    # Check if it is ready to extract
    if_ready = requests.get('http://ip/getready')
    if (if_ready.text == "ready"):

        # If the paths do not already exist for the processing create them
        if not os.path.exists("./" + str(count)):
            os.mkdir("./"+ str(count))
            os.mkdir("./"+ str(count) +"/current")
            os.mkdir("./"+ str(count) +"/extraction")

        # Extract the file
        patoolib.extract_archive("upload/file.zip", outdir="./"+ str(count) +"/extraction", interactive=False)
        os.remove("upload/file.zip")

        # Remove from queue 
        requests.get("http://ip/removequeue")

        # Start job with extracted file
        txt = os.system("bash job.sh " + str(count))
        count += 1
    time.sleep(0.5)
