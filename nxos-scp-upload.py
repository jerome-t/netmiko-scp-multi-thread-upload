#!/usr/bin/python
from netmiko import ConnectHandler, file_transfer
from netmiko.ssh_exception import NetMikoAuthenticationException, NetMikoTimeoutException
from paramiko.ssh_exception import AuthenticationException
from getpass import getpass
from argparse import ArgumentParser
import os.path

# --- Check file exists function
def __is_valid_file(parser, arg):
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


# --- Init argparse
parser = ArgumentParser()
parser.add_argument("filename", help="The file to upload", metavar='FILE', type=lambda x: __is_valid_file(parser, x))
args = parser.parse_args()

# --- Define the OS file to upload
SOURCE_FILE = (args.filename)

# --- Define the switch list
SW_LIST = []
with open("./hosts.txt", 'r') as FILE:
    SW_LIST = [line.rstrip() for line in FILE]

# --- Ask confirmation
print(80*"=")
print('Please, confirm the upload of:',SOURCE_FILE+' on: ')
print('note: if the file already exists, it will be overwritten.')
print(*SW_LIST, sep ='\n')
prompt = str("Proceed?")

if confirm(prompt=prompt, resp=False) == True:
    # --- Get credentials
    print(80*"-")
    USERNAME = input('Please insert your NX-OS username: ')
    print("And your password")
    PASSWORD = getpass()
    print(80*"-")

    # --- SCP itself
    for HOST in SW_LIST:
        net_device = {
        'device_type': 'cisco_nxos',
        'host': HOST,
        'username': USERNAME,
        'password': PASSWORD,
        }
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
            print(80*"-")
            print('Results for:', HOST)
            print('File exists already: ',transfer_dict['file_exists'])
            print('File transferred: ',transfer_dict['file_transferred'])
            print('MD5 verified :',transfer_dict['file_verified'])
            print(80*"=")
        except NetMikoTimeoutException:
            print('Skipped: SSH Timed out')
            print(80*"=")
            continue
        except (AuthenticationException, NetMikoAuthenticationException):
            print('Skipped: Authentication failed')
            print(80*"=")
            continue
    # --- All done confirmation
    print("List completed, goodbye.")
    print(80*"=")
else:
    print("Operation aborted, goodbye.")
    print(80*"=")
