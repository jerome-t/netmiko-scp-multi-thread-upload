# NX-OS-SCP-Bulk-Transfer

A Simple Python script to upload and verify (checksum) files to multiple Cisco NX-OS devices, with the support of Netmiko.

 
## Use Case Description

If you have a large number of NX-OS devices and need to upload a file, for example a new version of NX-OS, to all these devices without the help of an external tool like Cisco DCNM or similar, it can be very time-consuming. This script takes care of everything.

## Installation

Requirements: All you need is Python and pip. 
Then, with pip we will install Netmiko and dependencies.

Installation:

	$ git clone https://github.com/jerome-t/nxos-scp-upload.git
	$ sudo pip install -r requirements.txt

## Configuration

Update the file hosts.txt with the list of your NX-OS hosts, one host per line.

Example:

	host01.example.com
	host02.example.com

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
	n9300-testA.example.com
	n9300-testB.example.com
	Proceed? [n]|y: y
	--------------------------------------------------------------------------------
	Please insert your NX-OS username: admin
	And your password
	Password: 
	--------------------------------------------------------------------------------
	Upload on: n9300-testA.example.com
	--------------------------------------------------------------------------------
	Results for: n9300-testA.example.com
	File exists already:  False
	File transferred:  True
	MD5 verified : True
	================================================================================
	Upload on: n9300-testB.example.com
	--------------------------------------------------------------------------------
	Results for: n9300-testB.example.com
	File exists already:  True
	File transferred:  False
	MD5 verified : True
	================================================================================
	List completed, goodbye.
	================================================================================

	

### DevNet Sandbox

A great way to make your repo easy for others to use is to provide a link to a [DevNet Sandbox](https://developer.cisco.com/site/sandbox/) that provides a network or other resources required to use this code. In addition to identifying an appropriate sandbox, be sure to provide instructions and any configuration necessary to run your code with the sandbox.

## How to test the software

Provide details on steps to test, versions of components/dependencies against which code was tested, date the code was last tested, etc. 
If the repo includes automated tests, detail how to run those tests.
If the repo is instrumented with a continuous testing framework, that is even better.


## Known issues

Document any significant shortcomings with the code. If using [GitHub Issues](https://help.github.com/en/articles/about-issues) to track issues, make that known and provide any templates or conventions to be followed when opening a new issue. 

## Getting help

Instruct users how to get help with this code; this might include links to an issues list, wiki, mailing list, etc.

**Example**

If you have questions, concerns, bug reports, etc., please create an issue against this repository.

## Getting involved

This section should detail why people should get involved and describe key areas you are currently focusing on; e.g., trying to get feedback on features, fixing certain bugs, building important pieces, etc. Include information on how to setup a development environment if different from general installation instructions.

General instructions on _how_ to contribute should be stated with a link to [CONTRIBUTING](./CONTRIBUTING.md) file.

## Author(s)

This project was written and is maintained by the following individuals:

* Jerome Tissieres <jerome@tissieres.ch>
