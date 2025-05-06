import requests
import json
from socautomationfunctions import retrieve_Sign_In_Logs_For_Account_EntraID
from socautomationfunctions import return_raw_string
import sys
from socautomationfunctions import parse_input_user_format


#Read in input
list_of_account_objects=parse_input_user_format('csv',return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/accounts.csv'))
if not list_of_account_objects:
    print("Failed to properly read in accounts")
    sys.exit(0)
print("Starting process to retrieve Sign-In logs for each account")

#retrieve_Sign_In_Logs_For_Account_EntraID for each Entra Account
for account_object in list_of_account_objects:
    retrieve_Sign_In_Logs_For_Account_EntraID(account_object,7,True)
print("Workflow complete. Please see output report to view workflow results.")
