#!/usr/bin/python
from getpass import getpass
from argparse import ArgumentParser
import csv
import os.path
import sys
from time import time
from concurrent.futures import ProcessPoolExecutor, wait
from netmiko import ConnLogOnly, file_transfer

# --- Define the threads
MAX_THREADS = 8

# --- Check file exists function
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return(arg)

# --- Confirmation function
def confirm(prompt=None, resp=False):

    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')

    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print ('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False


# --- Upload Netmiko function
def upload_nemiko(net_device):
    print("Upload on %s:" % net_device.get('host'))

    # Create the Netmiko SSH connection
    ssh_conn = ConnLogOnly(**net_device)

    # Test access, skip if failed
    if ssh_conn is None:
        print("Logging in failed... skipping")
        print(40*"-")
    else:
        transfer_dict = {}
        transfer_dict = file_transfer(ssh_conn,
                            source_file=SOURCE_FILE,
                            dest_file=SOURCE_FILE,
                            )
        print(80*"=")
        print('Results for %s:' % net_device.get('host'))
        print('File exists already: ',transfer_dict['file_exists'])
        print('File transferred: ',transfer_dict['file_transferred'])
        print('MD5 verified :',transfer_dict['file_verified'])

# --- Init argparse
parser = ArgumentParser()
parser.add_argument("filename", help="The file to upload", metavar='FILE', type=lambda x: is_valid_file(parser, x))
args = parser.parse_args()

# --- Define the OS file to upload
SOURCE_FILE = (args.filename)

# --- Check the hosts.csv file and get the list of hosts
VENDORS_TYPES = ["cisco_ios", "arista_eos", "juniper_junos", "cisco_nxos"]
VENDOR_TYPE = ''
HOSTS_LIST = []

with open("./hosts.csv", 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for row in csv_reader:
        if VENDOR_TYPE in VENDORS_TYPES not in str(row[1]):
            print('Invalid CSV, please check the vendor types. Must be: cisco_ios, arista_eos, juniper_junos or cisco_nxos')
            sys.exit()
        HOSTS_LIST.append(row[0])

# --- Ask confirmation
print(80*"=")
print('Please, confirm the upload of',SOURCE_FILE+' on: ')
print(*HOSTS_LIST, sep ='\n')
prompt = str("Proceed?")

if confirm(prompt=prompt, resp=False) == True:
    # --- Get credentials
    print(80*"-")
    USERNAME = input('Please insert your username: ')
    print("And your password")
    PASSWORD = getpass()
    print(80*"-")

    # --- Get the time for timing
    start_time = time()

    # --- Set the number of threads
    pool = ProcessPoolExecutor(MAX_THREADS)

    # --- SCP itself, in multi-threads
    SW_LIST = []
    FUTURE_LIST = []
    with open("./hosts.csv", 'r') as csvfile:
        SW_LIST = csv.reader(csvfile, delimiter=',')
        for CSV_ROW in SW_LIST:
            HOST = CSV_ROW[0]
            DEVICE_TYPE = CSV_ROW[1]
            net_device = {
            'device_type': DEVICE_TYPE,
            'host': HOST,
            'username': USERNAME,
            'password': PASSWORD,
            }
            FUTURE = pool.submit(upload_nemiko, net_device)
            FUTURE_LIST.append(FUTURE)

        wait(FUTURE_LIST)

    # --- All done confirmation
    print(80*"=")
    print("Uploads completed in {} seconds.".format(time() - start_time))
    print(80*"=")
else:
    print("Operation aborted, goodbye.")
    print(80*"=")
