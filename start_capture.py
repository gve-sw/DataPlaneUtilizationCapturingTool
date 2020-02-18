"""
Copyright (c) 2019 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

ISR Montiroing via command

Created on Fri Feb 14 10:10:20 2020

Script to inovke command in the remote shell with specified intervals and to capture the data in log/csv file.
"show platform hardware qfp active datapath utilization"

@author: rmalyava

"""

import os
import sys
import time
import signal
import threading

from datetime import datetime
from pathlib import Path

# Get the absolute path for the directory where this file is located
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

import channel
import devices

# Output Directory for the script
output_dir="logs"
command_to_execute_remotely = "show platform hardware qfp active datapath utilization"


# Method for Appending the command output to the file
def write_to_file(filename,content,ext=".log"):
	# Create the output folder if not available
	Path(output_dir).mkdir(parents=True, exist_ok=True)
	output_file=output_dir+"/"+filename+'-'+time.strftime('%Y-%m-%d')+ext
	with open(output_file,'a') as f:
		f.write(content)

# Method to create remote shell on the device
def remote_command_capture(device_info):
	try:
		print("{} : Trying SSH ...".format(device_info['alias']))
		remote_ssh = channel.channel(str(device_info['host']),str(device_info['username']),str(device_info['password']))
		print("{} : Remote Shell acquired.".format(device_info['alias']))
		invoke_command_scheduled(remote_ssh,device_info)
	except Exception as error:
		print("{} : {}, not able to capture ".format(device_info['alias'],error))

# Method to invoke the command in specified intervals of time
def invoke_command_scheduled(ssh,device_info):
	print("{} : Capture started ... with interval of {} seconds".format(device_info['alias'],device_info['interval']))
	while(True):
		output=ssh.sendCommand(command_to_execute_remotely)
		write_to_file(device_info['alias'],output)
		time.sleep(int(device_info['interval']))

def signal_handler(signal, frame):
	print('stopping capture of utilization ...')
	sys.exit(0)

# Steps to invoke when the script is invoked
if __name__ == "__main__":
	signal.signal(signal.SIGINT,signal_handler)
	pooling_length=len(devices.DEVICE_LIST)
	print("Found {} devices\nfind logs at {}".format(pooling_length,os.path.abspath(output_dir)))
	jobs = []
	for device in devices.DEVICE_LIST:
		p = threading.Thread(target=remote_command_capture,args=(device,))
		jobs.append(p)
		p.start()
