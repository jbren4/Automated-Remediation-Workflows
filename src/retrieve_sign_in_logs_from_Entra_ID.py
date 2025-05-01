import requests
import json
from socautomationfunctions import retrieve_Sign_In_Logs_For_Account_EntraID
from socautomationfunctions import return_raw_string

#Read in ndJSON objects
print(f"Attempting to read in Account objects")
list_of_accounts_to_retrieve_signInLogs=[]
with open(return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/accounts.json'),'r') as file_obj:
    list_of_accounts_to_retrieve_signInLogs=file_obj.readlines()
print("Successfully read in input file")

#Convert each ndJSON string to a Python dictionary
list_of_accounts_to_retrieve_signInLogs=[ json.loads(line) for line in list_of_accounts_to_retrieve_signInLogs ]

print("Starting process to retrieve Sign-In logs for each account")
for account_object in list_of_accounts_to_retrieve_signInLogs:
    retrieve_Sign_In_Logs_For_Account_EntraID(account_object,7,True)
print("Workflow complete. Please see output report to view workflow results.")
