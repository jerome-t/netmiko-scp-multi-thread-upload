# nxos-scp-upload

Here is a very simple Python script to upload and verify files to Cisco NX-OS hosts with Netmiko.

It's very simple, just specify two things:
- The nxos hosts at line 6 - here it's a simple list, but this can be changed to an inventory file or anything else.
- The nxos file name and location at line 9

Then, at each host, a confirmation is requested before the upload.
At the end of each upload, there's a MD5 checksum control.

The original script from Kirk Byers is available here: https://pynet.twb-tech.com/blog/automation/netmiko-scp.html


Jerome Tissieres
https://aboutnetworks.net
