import json
from socautomationfunctions import trigger_MDE_AV_Scan
from socautomationfunctions import return_raw_string


#Read in input hosts stored nDJSON file
print("Attempting to read in host objects")
list_of_hosts_to_scan=[]
with open(return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/hosts.json'),'r') as file_obj:
    list_of_hosts_to_scan=file_obj.readlines()
print("Successfully read in input file of host objects")

list_of_hosts_to_scan=[json.loads(str_dict) for str_dict in list_of_hosts_to_scan]

#For each input Defender host_id, trigger MDE scan
print("Now triggering MDE scan for hosts")
for host_obj in list_of_hosts_to_scan:
    trigger_MDE_AV_Scan(host_obj.get('host_id'),'Quick',"Quick MDE Scan")
print("Workflow complete. Please see output report to view workflow results.")
