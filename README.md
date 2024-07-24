# Twitter Internet Archive Holidays Analysis
This project downloads data from [Internet Archive](https://archive.org/details/twitterstream). Multiple "worker" servers download these files since the Internet Archive sets a low download speed. Then a Proxy server acts like a man in the middle between the Worker servers and the supercomputer Siku. The proxy manages when worker servers should upload their file to the supercomputer and when the supercomputer has finished submitting a job. 
![diagram](Diagram.png "Diagram")
