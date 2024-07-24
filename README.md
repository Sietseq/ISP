# Twitter Internet Archive Holidays Analysis
This project downloads data from [Internet Archive](https://archive.org/details/twitterstream). Multiple "worker" servers download these files since the Internet Archive sets a low download speed. Then a Proxy server acts like a man in the middle between the Worker servers and the supercomputer Siku. The proxy manages when worker servers should upload their file to the supercomputer and when the supercomputer has finished submitting a job. \
![diagram](diagram.png "Diagram")

## Worker 
This portion downloads the files to then be processed by the super computer. This can be ran on multiple cloud instances to get around the download limit imposed by the Internet Archive. To run this:
```
$ sudo apt install python3-venv 
$ python3 -m venv .venv 
$ source .venv/bin/activate 
$ pip install progressbar requests && 
$ mkdir download
$ touch files.txt  
$ sudo apt install sshpass
```
You will also have to go into ```worker.py``` and edit the proxy ip used and the username used for Siku.. Be sure to login at least to generate a fingerprint for the scp process.
