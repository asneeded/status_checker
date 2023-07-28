import sys
import requests
import logging
import concurrent.futures
import socket
from os import system, name
import argparse

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
{bcolors.OKBLUE}____ ___ ____ ___ _  _ ____ ____ _  _ ____ ____ _  _ ____ ____ 
{bcolors.OKCYAN}[__   |  |__|  |  |  | [__  |    |__| |___ |    |_/  |___ |__/ 
{bcolors.OKGREEN}___]  |  |  |  |  |__| ___] |___ |  | |___ |___ | \_ |___ |  \ {bcolors.WARNING}Ver. {__version__}
"""
banner += "_" * 70 + '\n' 
banner += f"{bcolors.OKBLUE}Author: {__author__} \t{bcolors.OKCYAN}License: {__license__}{bcolors.ENDC}\n\n"
banner += f"{bcolors.WARNING}_" * 70 + f'{bcolors.ENDC}\n'

def ip_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
    except Exception as e:
        logging.error(e)
        ip = None
    return ip


def open_file(file):
    try:
        with open(file) as fh:
            content = fh.readlines()
        domains = [ x.strip() for x in content]
        return domains
    except Exception as e:
        print(f'{bcolors.FAIL}[!] {e}{bcolors.ENDC}')
        sys.exit(1)

def write_to_file(good_urls):
    with open(args.output, 'w') as fp:
        for domain, items in good_urls.items():
            fp.write("%s\t\t%s\t\t%s\n" % (items[1], domain, items[0]))

def get_status(uri):
    ip = ip_lookup(uri)
    url = 'http://' + uri
   
    try:
        r = requests.head(url, timeout=5)
        if r.status_code == 200 or r.status_code == 301 or r.status_code == 302:
            
            print(bcolors.OKGREEN + '[+]', ip, uri,  r.status_code, sep='\t')
            good_urls[uri] = [r.status_code, ip]
        elif str(r.status_code[0]) == '4':
            good_urls[uri] = [r.status_code, ip]
            print(bcolors.WARNING +'[+]',ip ,uri, r.status_code, sep = '\t')
        else:  
            print(bcolors.FAIL +'[-]',uri, r.status_code)

    except Exception as e:
        logging.error(e)

    
if __name__ == '__main__':
    format = '%(asctime)s: %(message)s'
    logging.basicConfig(filename='app.log', filemode='a',format=format, level=logging.INFO, datefmt="%H:%M:%S")
    parser = argparse.ArgumentParser(description='Check the status of a list of domains')
    parser.add_argument('-f','--file', help='File containing list of domains')
    parser.add_argument('-o', '--output', help='Output file', required=False)   
    args = parser.parse_args()
    if name == 'nt':
        system('cls')
    else:
        system('clear')
    print(bcolors.HEADER + banner + bcolors.ENDC)
   
    good_urls = {}


    domains = open_file(args.file)



    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executer:
        executer.map(get_status, domains)

    if args.output:
        write_to_file(good_urls)
