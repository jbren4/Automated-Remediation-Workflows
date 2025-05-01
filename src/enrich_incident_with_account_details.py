from socautomationfunctions import Enrich_Account_Values
import pandas as pd
import json
import os
import requests
import sys
from socautomationfunctions import return_raw_string


list_of_account_objects=None
with open('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/accounts.json','r') as file_obj:
    list_of_account_objects=file_obj.readlines()

list_of_account_objects=[json.loads(line)   for line in list_of_account_objects]

list_of_logs_objects=[]
#Iterate through the accounts that are going to be enriched
for account_to_enrich in list_of_account_objects:
    list_of_logs_objects.append(Enrich_Account_Values("JSON",account_to_enrich,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
    
with open(return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/outputfiles/enriched_directory_accounts.json'),'w') as file_obj:
    for line in list_of_logs_objects:
        file_obj.write(json.dumps(line))
        file_obj.write('\n')

