import os
import urllib.request
import progressbar
import requests
import time
import ast

import subprocess


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
    if not os.path.exists('download/'):
        os.mkdir('download/')
    with open('files.txt') as read_file:
        for line in read_file:
            base_name = line.split('/')[-1].split('.')[0]
            print('Downloading: ' + line)
            urllib.request.urlretrieve(line, 'download/archive.zip' , show_progress)

            print('Uploading')
            requests.get('http://52.14.130.151/addqueue?file=' + base_name)
            ready = False
            while(not ready):
                my_list = requests.get('http://52.14.130.151/checkqueue')
                my_list = ast.literal_eval(my_list.text)
                if (my_list[1] == base_name):
                    print(base_name)
                    ready = True
                    text = os.system("sshpass -p 'pwd' scp ./download/archive.zip" + ' usr@siku.ace-net.ca:~/ISP/Siku/upload/file.zip ')
                    requests.get('http://52.14.130.151/setready')
                time.sleep(0.5)
            os.remove('download/archive.zip')


if __name__ == '__main__':
    main()
