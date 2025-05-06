import json
from socautomationfunctions import revoke_MFA_Methods
from socautomationfunctions import return_raw_string
list_of_json_user_objects=[]
from socautomationfunctions import parse_input_user_format
import sys


#Read in input file
list_of_account_objects=parse_input_user_format('csv',return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/accounts.csv'))
if not list_of_account_objects:
    print("Failed to properly read in accounts")
    sys.exit(0)


#For each input account object, attempt to revoke the account's MFA methods
print("Starting workflow to revoke MFA method enrollment")
for dictionary_account_object in list_of_account_objects:
    revoke_MFA_Methods(dictionary_account_object)
print("Workflow complete. Please see output report to view workflow results.")
