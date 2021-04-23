# netmiko-scp-multi-thread-upload

This script leverages Netmiko's features to secure copy (SCP) a single file to multiple remote network devices in parallel.
It checks if the file already exists on the remote devices and compares the checksums. If the files are identical, it does not upload it.


## Use Case Description

If you have a large number of network devices and need to upload a big file, like a new OS or similar, to all these devices, it can be very time-consuming. This script takes care of everything.

Supported devices are: Cisco IOS/IOS-XE/IOS-XR/NX-OS, Arista EOS, and Juniper JunOS.


## Installation

Requirements: All you need is Python and pip.
Then, with pip we will install Netmiko and dependencies.

Installation:

	$ git clone https://github.com/jerome-t/netmiko-scp-multi-thread-upload
	$ sudo pip install -r requirements.txt

## Configuration

Update the **hosts.csv** file with the list of your network hosts and vendor type.

Vendor types are: cisco_ios, arista_eos, juniper_junos, cisco_nxos

Example of hosts.csv:

	host01.example.com,cisco_ios
	host02.example.com,cisco_nxos


The file system used for each OS type is the one defined by default in Netmiko. Please refer to the Netmiko documentation here: https://pynet.twb-tech.com/blog/automation/netmiko-scp.html


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



## DevNet Sandbox

--- To be completed ---

A great way to make your repo easy for others to use is to provide a link to a [DevNet Sandbox](https://developer.cisco.com/site/sandbox/) that provides a network or other resources required to use this code. In addition to identifying an appropriate sandbox, be sure to provide instructions and any configuration necessary to run your code with the sandbox.


## How to test the software

--- To be completed ---

Provide details on steps to test, versions of components/dependencies against which code was tested, date the code was last tested, etc. 
If the repo includes automated tests, detail how to run those tests.
If the repo is instrumented with a continuous testing framework, that is even better.


## Known issues

The 'file exists already' value is always True, even if it does not exists in reality. The upload is done anyway, this is only an output error, but the script is working at 100%

This script uses multi-threads, it may be improved by using multi-processing.
The defined threads are 4 for now, I have to test what is the optimal number of threads depending on the devices, computer, network bandwidth and latency, etc.


## Getting help and Getting involved

Please contact me on [Twitter](https://twitter.com/JeromeTissieres) or open an Issue/P.R.

## Author(s)

This project was written and is maintained by the following individuals:

* Jerome Tissieres <jerome@tissieres.ch>
