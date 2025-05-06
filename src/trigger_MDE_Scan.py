import json
from socautomationfunctions import trigger_MDE_AV_Scan
from socautomationfunctions import return_raw_string
from socautomationfunctions import parse_input_host_format
import sys

list_of_hosts_to_scan=parse_input_host_format('csv',return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/hosts.csv'))
if not list_of_hosts_to_scan:
    print("Failed to properly read in host_ids")
    sys.exit(0)

#For each input Defender host_id, trigger MDE scan
print("Now triggering MDE scan for hosts")
for host_obj in list_of_hosts_to_scan:
    trigger_MDE_AV_Scan(host_obj,'Quick',"Quick MDE Scan")
print("Workflow complete. Please see output report to view workflow results.")
