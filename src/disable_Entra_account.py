import requests
import json
from socautomationfunctions import disable_Entra_Account
from socautomationfunctions import return_raw_string
from socautomationfunctions import parse_input_user_format
import sys


#Read in input file
list_of_account_objects=parse_input_user_format('csv',return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/accounts.csv'))
if not list_of_account_objects:
    print("Failed to properly read in accounts")
    sys.exit(0)

print("Starting workflow to disable input accounts")
#For each input account dictionary, attempt to revoke the account
for account_object in list_of_account_objects:
    disable_Entra_Account(account_object)
print("Workflow complete. Please see output report to view workflow results.")
