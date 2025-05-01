import json
from socautomationfunctions import locate_account_within_directory
from socautomationfunctions import return_raw_string

list_of_account_objects=[]
with open(return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/accounts.json'),'r') as file_obj:
    list_of_account_objects=file_obj.readlines()
    


list_of_account_objects=[json.loads(line)  for line in list_of_account_objects ]
direcotry_object=None
for account in list_of_account_objects:
    direcotry_object=locate_account_within_directory(account,False)
    if direcotry_object:
        print(f"Located account: {direcotry_object.get('userPrincipalName')}")
    else:
        print(f"Account {account.get('Account')} is not a valid account within the directory")

