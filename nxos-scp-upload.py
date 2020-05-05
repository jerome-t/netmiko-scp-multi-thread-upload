#!/usr/bin/python
from netmiko import ConnectHandler, file_transfer
from getpass import getpass

# --- Define the switches (this could also come from a file or an external inventory)
sw_list = ['host1.test.net', 'host2.test.net', 'host3.test.net']

# --- Define the OS file to upload
source_file = "./put_your_nxos_file_here.bin"

# --- Define if we download (get) or upload (put) the file
direction = 'put'

# --- Get credentials
username = input('Please insert your Nexus username: ')
print("And your password")
password = getpass()

# --- SCP itself 
for host in sw_list:
    net_device = { 
    'device_type': 'cisco_nxos',
    'host': host,
    'username': username,
    'password': password,
    }
    print("Upload on:", host)
    pause = input("Hit enter to continue or Ctrl-C to stop: ")
    # Create the Netmiko SSH connection
    ssh_conn = ConnectHandler(**net_device)
    transfer_dict = {}
    transfer_dict = file_transfer(ssh_conn,
                        source_file=source_file, 
                        dest_file=source_file,
                        file_system='bootflash:', 
                        direction=direction,
                        overwrite_file=True)
    print(40*"-")
    print("Results for:", host)
    print("File exists already: ",transfer_dict['file_exists'])
    print("File transferred: ",transfer_dict['file_transferred'])
    print("MD5 verified :",transfer_dict['file_verified'])
    print(40*"=")

# --- All done confirmation
print("All copy are done")
print(40*"=")
