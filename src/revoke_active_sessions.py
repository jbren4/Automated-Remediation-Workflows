import requests
import json
from socautomationfunctions import revoke_active_sessions
from socautomationfunctions import return_raw_string

#Read input ndJSON file
print(f"Attempting to read in Account objects")
list_of_account_objects=[]
with open(return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/accounts.json'),'r') as file_obj:
    list_of_account_objects=file_obj.readlines()
print("Successfully read in input file")
#Convert each strline from the file into Pyton dictionary
    #Now we have a list of Python dictionaires where each entry is the input account object
list_of_account_objects=[json.loads(str_line) for str_line in list_of_account_objects]

print("Starting workflow to revoke active sessions")
#For each input account dictionary, attempt to revoke the account
for account_object in list_of_account_objects:
    revoke_active_sessions(account_object)
print("Workflow complete. Please see output report to view workflow results.")



