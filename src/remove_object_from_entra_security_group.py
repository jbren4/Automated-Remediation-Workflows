import requests
import json
from socautomationfunctions import remove_Entra_Account_From_Enta_Group
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

#Read in group_ID
target_group_id=""

print("Starting workflow to remove Entra Objects from Entra Group")
for account_object in list_of_account_objects:
    remove_Entra_Account_From_Enta_Group(account_object,target_group_id)
