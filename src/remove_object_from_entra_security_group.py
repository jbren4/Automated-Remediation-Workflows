import requests
import json
from socautomationfunctions import remove_Entra_Account_From_Enta_Group
from socautomationfunctions import return_raw_string
import sys
from socautomationfunctions import parse_input_user_format


#Read in input
list_of_account_objects=parse_input_user_format('csv',return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/accounts.csv'))
if not list_of_account_objects:
    print("Failed to properly read in accounts")
    sys.exit(0)

#Specify Target Group ID
target_group_id=""

print("Starting workflow to remove Entra Objects from Entra Group")
for account_object in list_of_account_objects:
    remove_Entra_Account_From_Enta_Group(account_object,target_group_id)
