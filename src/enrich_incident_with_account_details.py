from socautomationfunctions import Enrich_Account_Values
import pandas as pd
import json
import os
import requests
import sys

tenant_id=''
client_id=''
client_secret=''
path_to_json_file=r''
path_to_CSV_file=''
output_path=r''
oAuth_token=requests.post(url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/token",data={"resource":"https://graph.microsoft.com","grant_type":"client_credentials","client_id":client_id,"client_secret":client_secret}).json().get('access_token')
list_of_account_objects_that_will_be_enriched=[]
#Check if path to CSV exists
if os.path.exists(r''):
    with open(path_to_json_file,'r') as file_obj:
        list_of_account_objects_that_will_be_enriched=json.load(file_obj)
    print("JSON file exist")
elif os.path.exists(path_to_CSV_file):
    #pd.read_csv()
    print("CSV file exists")
else:
    print("No input file found")
    sys.exit(0)

#Obtain a list of all enabled accounts_within_the_directory
list_of_enabled_accounts=requests.get(url="https://graph.microsoft.com/v1.0/users",headers={"Authorization":f"Bearer {oAuth_token}"},params={"$filter":"accountEnabled eq true","$select":f"mailNickname,Userprincipalname,firstName,lastName,userType,companyName,department,employeeeId,officelocation,mail,mailNickname,Lastpasswordchangedatetime,Createddatetime,jobtitle,employeeId,officeLocation,state,postalCode,country"}).json().get('value')
list_of_logs_objects=[]
#Iterate through the accounts that are going to be enriched
for account_to_enrich in list_of_account_objects_that_will_be_enriched:
    account_JSON_Object={}
    #JSON and UPN account identifier
    if account_to_enrich.get('Account_Identifier') and  account_to_enrich.get('Account') and account_to_enrich.get('Account_Identifier').lower().replace(' ','') =="upn":
        Enrich_Account_Values("JSON",account_to_enrich.get('Account'),'userPrincipalName','',account_JSON_Object,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,list_of_enabled_accounts,oAuth_token)
        list_of_logs_objects.append(account_JSON_Object)
    #JSON and mailnickname
    elif account_to_enrich.get('Account_Identifier') and account_to_enrich.get('Account')   and account_to_enrich.get('Account_Identifier').lower().replace(' ','') =="mailnickname":
        Enrich_Account_Values("JSON",account_to_enrich.get('Account'),'mailNickname','',account_JSON_Object,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,list_of_enabled_accounts,oAuth_token)
        list_of_logs_objects.append(account_JSON_Object)
    #JSON and mail
    elif account_to_enrich.get('Account_Identifier') and account_to_enrich.get('Account')   and (account_to_enrich.get('Account_Identifier').lower().replace(' ','') =="email" or account_to_enrich.get('Account_Identifier').lower().replace(' ','') =="mail" ):
        Enrich_Account_Values("JSON",account_to_enrich.get('Account'),'mail','',account_JSON_Object,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,list_of_enabled_accounts,oAuth_token)
        list_of_logs_objects.append(account_JSON_Object)
    #JSON and employeeID
    elif account_to_enrich.get('Account_Identifier') and account_to_enrich.get('Account')   and account_to_enrich.get('Account_Identifier').lower().replace(' ','') =="employeeid":
        Enrich_Account_Values("JSON",account_to_enrich.get('Account'),'employeeId','',account_JSON_Object,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,list_of_enabled_accounts,oAuth_token)
        list_of_logs_objects.append(account_JSON_Object)

with open(output_path,'w')as file_obj:
    json.dump(list_of_logs_objects,file_obj,indent=3)
