import os
import urllib.request
import progressbar
import requests
import time
import ast

import subprocess

# Used to visualize the progress in downloading
pbar = None
def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

def main():
    # Open the file that has record of links to be downloaded. 
    with open('files.txt') as read_file:
        for line in read_file:
            # Make easier name
            base_name = line.split('/')[-1].split('.')[0]
            
            # Start downloading
            print('Downloading: ' + line)
            urllib.request.urlretrieve(line, 'download/archive.zip' , show_progress)

            # Add to queue
            print('Uploading')
            requests.get('http://52.14.130.151/addqueue?file=' + base_name)
            ready = False

            # Keep checking if it is possible to upload
            while(not ready):
                # If the file is first in queue start uploading
                my_list = requests.get('http://ip/checkqueue')
                my_list = ast.literal_eval(my_list.text)
                if (my_list[1] == base_name):
                    print(base_name)
                    ready = True
                    # Upload file
                    text = os.system("sshpass -p 'pwd' scp ./download/archive.zip" + ' usr@siku.ace-net.ca:~/ISP/Siku/upload/file.zip ')
                    # Notify that upload is done
                    requests.get('http://52.14.130.151/setready')
                time.sleep(0.5)
            os.remove('download/archive.zip')


if __name__ == '__main__':
    main()
