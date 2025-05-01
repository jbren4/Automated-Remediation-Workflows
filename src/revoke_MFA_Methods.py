import json
from socautomationfunctions import revoke_MFA_Methods
from socautomationfunctions import return_raw_string
list_of_json_user_objects=[]

#Read in input ndJSON file
print(f"Attempting to read in Account objects")
with open(r'/Users/josephbrennan/githubProjects/SOC_Automations/input_files/accounts.json','r') as file_obj:
    list_of_json_user_objects=file_obj.readlines()
print("Successfully read in input file")

#Convert each line from ndJSON file to a Python dictionary
    #Now I have a list of Python dictionaries
list_of_json_user_objects=[json.loads(strline)  for strline in list_of_json_user_objects]

#For each input account object, attempt to revoke the account's MFA methods
print("Starting workflow to revoke MFA method enrollment")
for dictionary_account_object in list_of_json_user_objects:
    revoke_MFA_Methods(dictionary_account_object)
print("Workflow complete. Please see output report to view workflow results.")
