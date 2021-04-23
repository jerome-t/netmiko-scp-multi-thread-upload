#!/usr/bin/python
from getpass import getpass
from argparse import ArgumentParser
import os.path
from time import time
from concurrent.futures import ProcessPoolExecutor, wait
from netmiko import ConnectHandler, file_transfer
from netmiko.ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException
from paramiko.ssh_exception import AuthenticationException

# --- Define the variables
SW_LIST = []
MAX_THREADS = 4
future_list = []


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
    print("Upload on:", HOST)
        # Create the Netmiko SSH connection
    try:
        ssh_conn = ConnectHandler(**net_device)
        transfer_dict = {}
        transfer_dict = file_transfer(ssh_conn,
                            source_file=SOURCE_FILE,
                            dest_file=SOURCE_FILE,
                            file_system='bootflash:',
                            direction='put',
                            overwrite_file=True)
        print('Results for:', HOST)
        print('File exists already: ',transfer_dict['file_exists'])
        print('File transferred: ',transfer_dict['file_transferred'])
        print('MD5 verified :',transfer_dict['file_verified'])
        print(80*"=")
    except NetMikoTimeoutException:
        print('Skipped: SSH Timed out')
        print(80*"=")
        #continue
    except (AuthenticationException, NetMikoAuthenticationException):
        print('Skipped: Authentication failed')
        print(80*"=")
        #continue

# --- Init argparse
parser = ArgumentParser()
parser.add_argument("filename", help="The file to upload", metavar='FILE', type=lambda x: is_valid_file(parser, x))
args = parser.parse_args()

# --- Define the OS file to upload
SOURCE_FILE = (args.filename)

# --- Define the switch list
with open("./hosts.txt", 'r') as FILE:
    SW_LIST = [line.rstrip() for line in FILE]

# --- Ask confirmation
print(80*"=")
print('Please, confirm the upload of:',SOURCE_FILE+' on: ')
print(*SW_LIST, sep ='\n')
prompt = str("Proceed?")

if confirm(prompt=prompt, resp=False) == True:
    # --- Get credentials
    print(80*"-")
    USERNAME = input('Please insert your NX-OS username: ')
    print("And your password")
    PASSWORD = getpass()
    print(80*"-")

    # --- Get the time for timing
    start_time = time()

    # --- Set the number of threads
    pool = ProcessPoolExecutor(MAX_THREADS)

    # --- SCP itself, in multi-threads
    for HOST in SW_LIST:
        net_device = {
        'device_type': 'cisco_nxos',
        'host': HOST,
        'username': USERNAME,
        'password': PASSWORD,
        }
        future = pool.submit(upload_nemiko, net_device)
        future_list.append(future)

    wait(future_list)

    # --- All done confirmation
    print("Uploads completed in {} seconds.".format(time() - start_time))
    print(80*"=")
else:
    print("Operation aborted, goodbye.")
    print(80*"=")
