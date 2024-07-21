import os
import urllib.request
import progressbar
import requests
import time
import ast


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
    if not os.path.exists("download/"):
        os.mkdir("download/")
    with open('files.txt') as read_file:
        for line in read_file:
            base_name = line.split('/')[-1].split('.')[0]
            print("Downloading")
            urllib.request.urlretrieve(line, "download/archive" + line[len(line)-4:] , show_progress)
                
            print("Uploading")
            requests.get('http://52.14.130.151/addqueue?file=' + base_name)
            ready = False
            while(not ready):
                my_list = list(requests.get('http://52.14.130.151/checkqueue'))
                if (ast.literal_eval(my_list[0].decode())[1] == base_name):
                    print("yes!")
                    ready = True
                    os.popen("sshpass -p 'EvyeLAd7avFuv' scp ./download/archive" + line[len(line)-4:] + " an-sdebacker@siku.ace-net.ca:upload/file.tar ")
                    requests.get('http://52.14.130.151/setready')
                    time.sleep(0.5)
            

if __name__ == '__main__':
    main()