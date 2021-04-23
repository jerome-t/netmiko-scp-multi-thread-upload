# NX-OS-SCP-Bulk-Transfer

A Simple Python script to upload and verify (checksum) files to multiple network devices in parallel, supported by Netmiko

 
## Use Case Description

If you have a large number of NX-OS devices and need to upload a file, for example a new version of NX-OS, to all these devices without the help of an external tool like Cisco DCNM or similar, it can be very time-consuming. This script takes care of everything.

This script uses the strength and functionality of Netmiko to copy, in parallel, a single file to multiple network devices.

Supported devices are:

	Cisco Cisco IOS/IOS-XE/IOS-XR/NX-OS, Arista EOS, Juniper JunOS


## Installation

Requirements: All you need is Python and pip. 
Then, with pip we will install Netmiko and dependencies.

Installation:

	$ git clone https://github.com/jerome-t/nxos-scp-upload.git
	$ sudo pip install -r requirements.txt

## Configuration

Update the file hosts.csv with the list of your network hosts, one host per line, including the vendor type..

Vendor types are:

	cisco_ios
	arista_eos
	juniper_junos
	cisco_nxos

Example:

	host01.example.com,cisco_ios
	host02.example.com,cisco_nxos

The file system is the default defined into Netmiko. Please refer to the Netmiko documentation here[https://pynet.twb-tech.com/blog/automation/netmiko-scp.html]

## Usage

Add the file name as an argument to the script. 
Then, the script will check if the file exists, read the list of hosts and ask you for your NX-OS credentials in order to upload the file.
It will ask you for a confirmation before starting the upload.
To save time and bandwidth, if the file already exists it will be not overwritten.

usage: nxos-scp-upload.py filename

positional arguments:
  filename        The file to upload

Example where the file does not exists on the first host, but exists on the second:

	$ ./nxos-scp-upload.py testfile.txt 
	================================================================================
	Please, confirm the upload of: testfile.txt on: 
	n9300-labc.example.com
	n9300-labd.example.ch
	n9300-labe.example.ch
	n9300-labf.example.ch
	Proceed? [n]|y: y
	--------------------------------------------------------------------------------
	Please insert your NX-OS username: admin
	And your password
	Password: 
	--------------------------------------------------------------------------------
	Upload on: n9300-labc.example.ch
	Upload on: n9300-labd.example.ch
	Upload on: n9300-labe.example.ch
	Upload on: n9300-labf.example.ch
	Results for: n9300-labf.example.ch
	File exists already:  True
	File transferred:  True
	MD5 verified : True
	================================================================================
	Results for: n9300-labd.example.ch
	File exists already:  True
	File transferred:  True
	MD5 verified : True
	================================================================================
	Results for: n9300-labe.example.ch
	File exists already:  True
	File transferred:  True
	MD5 verified : True
	================================================================================
	Results for: n9300-labc.example.ch
	File exists already:  True
	File transferred:  True
	MD5 verified : True
	================================================================================
	Uploads completed in 3.500903606414795 seconds.
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

The MD5 check part need to be completed, it's not working yet.

This script uses multi-threads and may be improved by using multi-processing. 
The defined threads are 4 for now, I have to test what is the optimal number of threads depending on the devices, computer, network bandwidth and latency, etc.


## Getting help and Getting involved

Please contact me on [Twitter](https://twitter.com/JeromeTissieres) or open an Issue/P.R.

## Author(s)

This project was written and is maintained by the following individuals:

* Jerome Tissieres <jerome@tissieres.ch>
