import sys
import requests
import logging
import concurrent.futures
from os import system, name

__author__ = "Adam Sneed"
__copyright__ = "Copyright (C) 2023 Adam Sneed"
__license__ = "MIT License"
__version__ = "1.0"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

banner = f"""
____ ___ ____ ___ _  _ ____ ____ _  _ ____ ____ _  _ ____ ____ 
[__   |  |__|  |  |  | [__  |    |__| |___ |    |_/  |___ |__/ 
___]  |  |  |  |  |__| ___] |___ |  | |___ |___ | \_ |___ |  \ {__version__}
"""




def get_status(uri):
   
    try:
        r = requests.head(uri, timeout=5)
        if r.status_code == 200:
            
            print(bcolors.OKGREEN + '[+]', uri, r.status_code)
            good_urls.append(uri)
        else:
            print(bcolors.FAIL +'[-]',uri, r.status_code)

    except Exception as e:
        logging.error(e)

    
if __name__ == '__main__':
    format = '%(asctime)s: %(message)s'
    logging.basicConfig(filename='app.log', filemode='a',format=format, level=logging.INFO, datefmt="%H:%M:%S")
    if name == 'nt':
        system('cls')
    else:
        system('clear')
    print(bcolors.HEADER + banner + bcolors.ENDC)
    good_urls = []

    with open(sys.argv[1]) as fh:
        content = fh.readlines()
    domains = [ x.strip() for x in content]
    http_url = []
    https_url = []

    for domain in domains:
        http_url.append('http://' + domain)
        https_url.append('https://' + domain)
    
    # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executer:
    #     executer.map(get_status, http_url)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executer:
        executer.map(get_status, https_url)

    with open('good_urls.txt', 'w') as fp:
        for item in good_urls:
            fp.write("%s\n" % item)
