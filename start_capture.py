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


# Headers for the CSV file
csv_header_input="Input:Priority(pps)-5 secs,Input:Priority(pps)-1 min,Input:Priority(pps)-5 min,Input:Priority(pps)-60 min,Input:Priority(bps)-5 secs,Input:Priority(bps)-1 min,Input:Priority(bps)-5 min,Input:Priority(bps)-60 min,Input:Non-Priority(pps)-5 secs,Input:Non-Priority(pps)-1 min,Input:Non-Priority(pps)-5 min,Input:Non-Priority(pps)-60 min,Input:Non-Priority(bps)-5 secs,Input:Non-Priority(bps)-1 min,Input:Non-Priority(bps)-5 min,Input:Non-Priority(bps)-60 min,Input:Total(pps)-5 secs,Input:Total(pps)-1 min,Input:Total(pps)-5 min,Input:Total(pps)-60 min,Input:Total(bps)-5 secs,Input:Total(bps)-1 min,Input:Total(bps)-5 min,Input:Total(bps)-60 min"
csv_header_output="Output:Priority(pps)-5 secs,Output:Priority(pps)-1 min,Output:Priority(pps)-5 min,Output:Priority(pps)-60 min,Output:Priority(bps)-5 secs,Output:Priority(bps)-1 min,Output:Priority(bps)-5 min,Output:Priority(bps)-60 min,Output:Non-Priority(pps)-5 secs,Output:Non-Priority(pps)-1 min,Output:Non-Priority(pps)-5 min,Output:Non-Priority(pps)-60 min,Output:Non-Priority(bps)-5 secs,Output:Non-Priority(bps)-1 min,Output:Non-Priority(bps)-5 min,Output:Non-Priority(bps)-60 min,Output:Total(pps)-5 secs,Output:Total(pps)-1 min,Output:Total(pps)-5 min,Output:Total(pps)-60 min,Output:Total(bps)-5 secs,Output:Total(bps)-1 min,Output:Total(bps)-5 min,Output:Total(bps)-60 min"
csv_header_processing="Processing:Load(pct)-5 secs,Processing:Load(pct)-1 min,Processing:Load(pct)-5 min,Processing:Load(pct)-60 min"


# Method for Appending the command output to the file
def write_to_file(filename,content,ext=".log"):
	# Create the output folder if not available
	Path(output_dir).mkdir(parents=True, exist_ok=True)
	output_file=output_dir+"/"+filename+'-'+time.strftime('%Y-%m-%d')+ext
	with open(output_file,'a') as f:
		f.write(content)

def write_to_csv(filename,content,ext=".csv"):
	# Create the output folder if not available
	Path(output_dir).mkdir(parents=True, exist_ok=True)
	output_file=output_dir+"/"+filename+'-'+time.strftime('%Y-%m-%d')+ext
	if os.path.exists(output_file)==False:
		# Writing the CSV Header for the first time only
		with open(output_file,'a') as f:
			f.write("{},{},{},{}\n".format('timestamp',csv_header_input,csv_header_output,csv_header_processing))
	data_to_write=str(datetime.now())+","+content
	with open(output_file,'a') as f:
		f.write(data_to_write)

# Method to check whether the word exist in the given sentence
def wordInLine(words_list,line):
	for word in words_list:
		if word in line:
			return True
	return False

# Transforming the command output to CSV
def transformOutputToCSV(content):
	contentLines=content.splitlines()
	contentLines = list(filter(None, contentLines))
	word_match_list=["datapath","CPP","terminal","show"]
	csvContent=""
	for line in contentLines:
		if wordInLine(word_match_list,line) != True:
			content_for_append="{},{},{},{}".format(line[23:36].strip(),line[37:50].strip(),line[51:64].strip(),line[65:78].strip())
			if(content_for_append.strip(',')!=''):
				if(csvContent!=""):
					csvContent+=","
				csvContent+=content_for_append
	return csvContent+"\n"

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
		write_to_csv(device_info['alias'],transformOutputToCSV(output.strip()))
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
