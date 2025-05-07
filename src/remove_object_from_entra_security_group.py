import requests
import json
from socautomationfunctions import remove_Entra_Account_From_Enta_Group
from socautomationfunctions import return_raw_string
import sys
from socautomationfunctions import parse_input_user_format
import pandas as pd


#Read in input
list_of_account_objects=parse_input_user_format('csv',return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/account_and_group.csv'))
if not list_of_account_objects:
    print("Failed to properly read in accounts")
    sys.exit(0)
    
#Read in CSV specifing target group ID
target_group_id=pd.read_csv(return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/account_and_group.csv'))['Group_ID'].to_list()[0]

if not target_group_id or not isinstance(target_group_id,str):
    print("Check input CSV format. Failed to find a valid string specifiying the Security Group's ObjectID")
    sys.exit(0)

print("Starting workflow to remove Entra Objects from Entra Group")
for account_object in list_of_account_objects:
    remove_Entra_Account_From_Enta_Group(account_object,target_group_id)
