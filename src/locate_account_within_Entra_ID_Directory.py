import json
from socautomationfunctions import locate_account_within_directory
from socautomationfunctions import return_raw_string
import sys
from socautomationfunctions import parse_input_user_format

list_of_account_objects=parse_input_user_format('csv',return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/accounts.csv'))
if not list_of_account_objects:
    print("Failed to find valid directory object for input accounts")
    sys.exit(0)

direcotry_object=None
for account in list_of_account_objects:
    direcotry_object=locate_account_within_directory(account,False)
    if direcotry_object:
        print(f"Located account: {direcotry_object.get('userPrincipalName')}")
    else:
        print(f"Account {account.get('Account')} is not a valid account within the directory")

