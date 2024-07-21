import requests
import patoolib
import os

count = 0
os.mkdir("./upload")
while(True):
    if_ready = requests.get('http://52.14.130.151/getready')
    if (bool(if_ready)):
        os.mkdir("./"+ str(count)) 
        os.mkdir("./"+ str(count) +"/current")
        os.mkdir("./"+ str(count) +"/extraction")
        patoolib.extract_archive("upload/file.tar", "./"+ str(count) +"/extraction")
        os.remove("upload/file.tar")
        requests.get("http://52.14.130.151/removequeue")
        os.popen("sbatch -D `pwd` --export=var_name='" + str(count) + "'job.sh")

