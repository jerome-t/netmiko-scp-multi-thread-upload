[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/jerome-t/netmiko-scp-multi-thread-upload)

# netmiko-scp-multi-thread-upload

This script leverages Netmiko's features to securely copy (SCP) a single file to a remote network device. It also checks if the file exists already on the remote device and compares the checksums: if the files are identical, it does not upload it.
To this, I added parallelism: to make copies in parallel towards several remote devices. And also to have the remote hosts and OS defined in a CSV file, to avoid having to edit the Python script itself. I also added a check if the file to copy is present locally.


## Use Case Description

If you have a large number of network devices to which you need to send a file, such as a new operating system or similar, doing it manually can be very time consuming. This script takes care of everything and does the upload in parallel to save time.

Supported devices are: Cisco IOS*/IOS-XE/IOS-XR/NX-OS, Arista EOS, and Juniper JunOS.

Remark: on Cisco IOS, only ascii files are supported. Modern Cisco OS (XE, XR, NXOS) are not affected.


## Installation

Requirements: All you need is Python and pip.
Then, with pip we will install Netmiko and dependencies.

Installation:

	$ git clone https://github.com/jerome-t/netmiko-scp-multi-thread-upload
	$ sudo pip install -r requirements.txt

## Configuration

Update the **hosts.csv** file with the list of your network hosts and vendor type.

Vendor types are: cisco_ios (valid for IOS/IOS-XE/IOS-XR), cisco_nxos, arista_eos, juniper_junos

Example of hosts.csv:

	host01.example.com,cisco_ios
	host02.example.com,cisco_nxos
	host03.example.com,arista_eos
	host04.example.com,juniper_junos


The file system used for each device type is the one defined by default in Netmiko:

	Cisco IOS/IOS-XE/IOS-XR        Auto detects the file-system
	Cisco NX-OS                    bootflash:
	Arista EOS                     /mnt/flash
	Juniper Junos                  /var/tmp


Please refer to the Netmiko documentation here for more information: https://pynet.twb-tech.com/blog/automation/netmiko-scp.html


## Usage

Add the filename as an argument to the script.

The script will also check if the file exists, then read the list of hosts, vendor type and ask you for your credentials.

It will ask you for a confirmation before starting the upload.

To save time and bandwidth, if the file already exists it will be not overwritten.

**Usage: scp-multi-upload.py filename**

positional arguments:
  filename        The file to upload

Example where the file does not exists on the first host, but exists on the second:

	$ ./scp-multi-upload.py testfile.txt
	================================================================================
	Please, confirm the upload of testfile.txt on: 
	c.example.com
	d.example.com
	e.example.com
	f.example.com
	Proceed? [n]|y: y
	--------------------------------------------------------------------------------
	Please insert your username: admin
	And your password
	Password: 
	--------------------------------------------------------------------------------
	Upload on: c.example.com
	Upload on: d.example.com
	Upload on: e.example.com
	Upload on: f.example.com
	================================================================================
	Results for c.example.com:
	File exists already:  True
	File transferred:  True
	MD5 verified : True
	================================================================================
	Results for f.example.com:
	File exists already:  True
	File transferred:  True
	MD5 verified : True
	================================================================================
	Results for e.example.com:
	File exists already:  True
	File transferred:  True
	MD5 verified : True
	================================================================================
	Results for d.example.com:
	File exists already:  True
	File transferred:  True
	MD5 verified : True
	================================================================================
	Uploads completed in 3.351285219192505 seconds.
	================================================================================



## How to test the software & DevNet Sandbox

You can test to transfer a file to a [DevNet Sandbox](https://developer.cisco.com/site/sandbox/) 
For example, you can change the file **hosts.csv** like below, to test with the CRS1000v (IOX-XE) always on sandbox:
	
	sandbox-iosxe-latest-1.cisco.com,cisco_ios

For the credentials, please check the [Cisco DevNet Sandbox](https://developer.cisco.com/site/sandbox/) and search for Always On Sandbox in the Sandbox catalog. 


## Known issues

The 'file exists already' return value is always True, even if the file does not exists on the remote device. The upload is done anyway, this is only an output error, but the script is working at 100%

This script uses multi-threads, it may be improved by using multi-processing.
The max. threads are 8 for now, I have to test what is the optimal number of threads depending on the devices, computer, network bandwidth and latency, etc.


## Getting help and Getting involved

Please contact me on [Twitter](https://twitter.com/JeromeTissieres) or open an Issue/P.R.

## Author(s)

This project was written and is maintained by the following individuals:

* Jerome Tissieres <jerome@tissieres.ch>
