import requests
import json
import datetime
import re
import os
from dotenv import load_dotenv
import pandas as pd
#Enrich the log with the following data from Entra ID Cloud Directory
    #userPrincipalName (UPN)
    #userType (Member/Guest)
    #createdDateTime (Account Creation Timestamp)
    #lastPasswordChangeDateTime (Account last password change timestamp)
    #jobTitle (Job Title)
    #companyName (Company Name)
    #department (Department)
    #employeeId (EmployeeID)
    #officeLocation (Physical Office Location)
    #state (State/Region)
    #postalCode (Zip Code)
    #country (Country of the user)
    #mail (Primary Email)
    #mailNickname (mailNickname)
    #Account's Manager (Adds the UPN of the account's manager to the log)
#Enriches the log based on the values of account fields
def Enrich_Account_Values(log_type,attribute_that_will_enrich_the_event_with,unique_account_identifier_attribute,name_of_field,log_object,list_of_UPNs,list_of_User_Types,list_of_Account_Creation_Dates,list_of_Last_Password_Change_Time,list_of_Job_Titles,list_of_company_name,list_of_Departments,list_of_employee_IDs,list_of_office_location,list_of_regions_for_accounts,list_of_zip_codes,list_of_employee_countries,list_of_primary_emails,list_of_mail_nicknames,list_of_managers,list_of_enabled_accounts_with_fields_to_enrich_on,bearer_token_for_graph_api_requests):
    directory_account=locate_account_within_directory(attribute_that_will_enrich_the_event_with,False)
    new_dict_for_directory_account={}
    if not directory_account:
        new_dict_for_directory_account[f'Original_Account_Value']=attribute_that_will_enrich_the_event_with.get('Account')
        new_dict_for_directory_account[f'UPN']="Account not found within Entra ID"
        new_dict_for_directory_account[f'User_Type']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Account_Creation_Date']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Last_Password_Change_TimeStamp']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Job_Title']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Company_Name']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Department']="Account not found within Entra ID"
        new_dict_for_directory_account[f'employee_Id']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Office_Location']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Region']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Postal_Code']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Country']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Email']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Mail_Nickname']="Account not found within Entra ID"
        new_dict_for_directory_account[f'Manager']="Account not found within Entra ID"
        print("Failure: Failed to identify a valid directory account with input. Please check input value and input format")
        return new_dict_for_directory_account
    new_dict_for_directory_account[f'Original_Account_Value']=attribute_that_will_enrich_the_event_with.get('Account')
    if directory_account.get('userPrincipalName'):
        new_dict_for_directory_account[f'UPN']=directory_account.get('userPrincipalName')
    else:
        new_dict_for_directory_account[f'UPN']="Not Found"
    if directory_account.get('userType'):
        new_dict_for_directory_account[f'User_Type']=directory_account.get('userType')
    else:
        new_dict_for_directory_account[f'User_Type']="Not Found"
    if directory_account.get('createdDateTime'):
        new_dict_for_directory_account[f'Account_Creation_Date']=directory_account.get('createdDateTime')
    else:
        new_dict_for_directory_account[f'Account_Creation_Date']="Not Found"
    if directory_account.get('lastPasswordChangeDateTime'):
        new_dict_for_directory_account[f'Last_Password_Change_TimeStamp']=directory_account.get('lastPasswordChangeDateTime')
    else:
        new_dict_for_directory_account[f'Last_Password_Change_TimeStamp']="Not Found"
    if directory_account.get('jobTitle'):
        new_dict_for_directory_account[f'Job_Title']=directory_account.get('jobTitle')
    else:
        new_dict_for_directory_account[f'Job_Title']="Not Found"
    if directory_account.get('companyName'):
        new_dict_for_directory_account[f'Company_Name']=directory_account.get('companyName')
    else:
        new_dict_for_directory_account[f'Company_Name']="Not Found"
    if directory_account.get('department'):
        new_dict_for_directory_account[f'Department']=directory_account.get('department')
    else:
        new_dict_for_directory_account[f'Department']="Not Found"
    if directory_account.get('employeeId'):
        new_dict_for_directory_account[f'employee_Id']=directory_account.get('employeeId')
    else:
        new_dict_for_directory_account[f'employee_Id']="Not Found"
    if directory_account.get('officeLocation'):
        new_dict_for_directory_account[f'Office_Location']=directory_account.get('officeLocation')
    else:
        new_dict_for_directory_account[f'Office_Location']="Not Found"
    if directory_account.get('state'):
        new_dict_for_directory_account[f'Region']=directory_account.get('state')
    else:
        new_dict_for_directory_account[f'Region']="Not Found"
    if  directory_account.get('postalCode'):
        new_dict_for_directory_account[f'Postal_Code']=directory_account.get('postalCode')
    else:
        new_dict_for_directory_account[f'Postal_Code']="Not Found"
    if directory_account.get('country'):
        new_dict_for_directory_account[f'Country']=directory_account.get('country')
    else:
        new_dict_for_directory_account[f'Country']="Not Found"
    if directory_account.get('mail'):
        new_dict_for_directory_account[f'Email']=directory_account.get('mail')
    else:
        new_dict_for_directory_account[f'Email']="Not Found"
    if directory_account.get('mailNickname'):
        new_dict_for_directory_account[f'Mail_Nickname']=directory_account.get('mailNickname')
    else:
        new_dict_for_directory_account[f'Mail_Nickname']="Not Found"
    bearer_token_for_graph_api_requests=obtain_oAuth_token_graph_API()
    manager_response_object=requests.get(url=f"https://graph.microsoft.com/v1.0/users/{directory_account.get('userPrincipalName')}/manager",headers={"authorization":f"Bearer {bearer_token_for_graph_api_requests}"})
    if manager_response_object.status_code==200:
        new_dict_for_directory_account[f'Manager']=manager_response_object.json().get('userPrincipalName')
    else:
        new_dict_for_directory_account[f'Manager']="Not Found"
    return new_dict_for_directory_account
    
    '''
    #Iterate through each enabled account with the directory
    for enabled_account in list_of_enabled_accounts_with_fields_to_enrich_on:
        #Account field within CSV log matches an account within the cloud directory. Thus enrich the CSV  log based on values extracted from the cloud directory
        if enabled_account.get(unique_account_identifier_attribute)!=None and enabled_account.get(unique_account_identifier_attribute).lower().replace(' ','')==attribute_that_will_enrich_the_event_with.lower().replace(' ','') and log_type=="CSV":
            account_already_enriched=True
            if enabled_account.get('userPrincipalName'):
                list_of_UPNs.append(enabled_account.get('userPrincipalName'))
            else:
                list_of_UPNs.append("Not Found")
            if enabled_account.get('userType'):
                list_of_User_Types.append(enabled_account.get('userType'))
            else:
                list_of_User_Types.append("Not Found")
            if enabled_account.get('createdDateTime'):
                list_of_Account_Creation_Dates.append(enabled_account.get('createdDateTime'))
            else:
                list_of_Account_Creation_Dates.append("Not Found")
            if enabled_account.get('lastPasswordChangeDateTime'):
                list_of_Last_Password_Change_Time.append(enabled_account.get('lastPasswordChangeDateTime'))
            else:
                list_of_Last_Password_Change_Time.append("Not Found")
            if enabled_account.get('jobTitle'):
                list_of_Job_Titles.append(enabled_account.get('jobTitle'))
            else:
                list_of_Job_Titles.append("Not Found")
            if enabled_account.get('companyName'):
                list_of_company_name.append(enabled_account.get('companyName'))
            else:
                list_of_company_name.append("Not Found")
            if enabled_account.get('department'):
                list_of_Departments.append(enabled_account.get('department'))
            else:
                list_of_Departments.append("Not Found")
            if enabled_account.get('employeeId'):
                list_of_employee_IDs.append(enabled_account.get('employeeId'))
            else:
                list_of_employee_IDs.append("Not Found")
            if enabled_account.get('officeLocation'):
                list_of_office_location.append(enabled_account.get('officeLocation'))
            else:
                list_of_office_location.append("Not Found")
            if enabled_account.get('state'):
                list_of_regions_for_accounts.append(enabled_account.get('state'))
            else:
                list_of_regions_for_accounts.append("Not Found")
            if  enabled_account.get('postalCode'):
                list_of_zip_codes.append(enabled_account.get('postalCode'))
            else:
                list_of_zip_codes.append("Not Found")
            if enabled_account.get('country'):
                list_of_employee_countries.append(enabled_account.get('country'))
            else:
                list_of_employee_countries.append("Not Found")
            if enabled_account.get('mail'):
                list_of_primary_emails.append(enabled_account.get('mail'))
            else:
                list_of_primary_emails.append("Not Found")
            if enabled_account.get('mailNickname'):
                list_of_mail_nicknames.append(enabled_account.get('mailNickname'))
            else:
                list_of_mail_nicknames.append("Not Found")
            manager_response_object=requests.get(url=f"https://graph.microsoft.com/v1.0/users/{enabled_account.get('userPrincipalName')}/manager",headers={"authorization":f"Bearer {bearer_token_for_graph_api_requests}"})
            if manager_response_object.status_code==200:
                list_of_managers.append(manager_response_object.json().get('userPrincipalName'))
            else:
                list_of_managers.append("Not Found")
        #Account field with JSON log matches an account within the cloud directory. Thus enrich the JSON log based on values extracted from the cloud directory
    #Account field within CSV log wasn't found within an account within the cloud directory. Thus indicate account not found
    if not account_already_enriched and log_type=="CSV":
        list_of_UPNs.append("Account not found within Entra ID")
        list_of_User_Types.append("Account not found within Entra ID")
        list_of_Account_Creation_Dates.append("Account not found within Entra ID")
        list_of_Last_Password_Change_Time.append("Account not found within Entra ID")
        list_of_Job_Titles.append("Account not found within Entra ID")
        list_of_company_name.append("Account not found within Entra ID")
        list_of_Departments.append("Account not found within Entra ID")
        list_of_employee_IDs.append("Account not found within Entra ID")
        list_of_office_location.append("Account not found within Entra ID")
        list_of_managers.append("Account not found within Entra ID")
        list_of_regions_for_accounts.append("Account not found within Entra ID")
        list_of_zip_codes.append("Account not found within Entra ID")
        list_of_employee_countries.append("Account not found within Entra ID")
        list_of_primary_emails.append("Account not found within Entra ID")
        list_of_mail_nicknames.append("Account not found within Entra ID")
   '''

#Validates that an input Python dictionary object represents a valid Entra ID directory object
    #account_object: Python dictionary object which represents an account we wish to validate exists within our Entra ID tenant
    #enabled_accounts_only: Boolean indicating if only enabled Entra ID directory accounts should be checked against the input Python dictionary
def locate_account_within_directory(account_object,enabled_accounts_only):
    oAuth_token=obtain_oAuth_token_graph_API()
    if not oAuth_token:
        print(f"Failure: Failed to locate account: {account_object} within the Entra ID Directory. Failed to obtain oAuth Token")
        return False
    list_of_user_account_response_object=None
    if enabled_accounts_only:
        list_of_user_account_response_object=requests.get(url="https://graph.microsoft.com/v1.0/users",headers={"Authorization":f"Bearer {oAuth_token}"},params={"$select":"mail,mailNickname,userPrincipalName,employeeId,accountEnabled,id,userType,createdDateTime,lastPasswordChangeDateTime,jobTitle,companyName,department,officeLocation,state,postalCode,country","$filter":"accountEnabled eq true"})
    else:
        list_of_user_account_response_object=requests.get(url="https://graph.microsoft.com/v1.0/users",headers={"Authorization":f"Bearer {oAuth_token}"},params={"$select":"mail,mailNickname,userPrincipalName,employeeId,accountEnabled,id,userType,createdDateTime,lastPasswordChangeDateTime,jobTitle,companyName,department,officeLocation,state,postalCode,country"})
    list_of_enabled_directory_accounts=[]
    #Valid accounts found
    if list_of_user_account_response_object.status_code==200:
        list_of_enabled_directory_accounts=list_of_user_account_response_object.json().get('value')
    else:
        print("Failure to return list of directory accounts from Entra ID. Issue with API call or network")
        return False
    #Attempt to identify a valid directory account
    for enabled_directory_account in list_of_enabled_directory_accounts:
        #If valid directory account found, return True
        if enabled_directory_account.get('mail') and enabled_directory_account.get('mail').lower().replace(' ','')==account_object.get('Account').lower().replace(' ',''):
            return enabled_directory_account
        elif  enabled_directory_account.get('mailNickname') and enabled_directory_account.get('mailNickname').lower().replace(' ','')==account_object.get('Account').lower().replace(' ',''):
            return enabled_directory_account
        elif  enabled_directory_account.get('userPrincipalName') and enabled_directory_account.get('userPrincipalName').lower().replace(' ','')==account_object.get('Account').lower().replace(' ',''):
            return enabled_directory_account
        elif enabled_directory_account.get('employeeId') and enabled_directory_account.get('employeeId').lower().replace(' ','')==account_object.get('Account').lower().replace(' ',''):
            return enabled_directory_account
    #Return False if no valid direcory account is found
    print(f"Failed to identify a valid directory account for input account {account_object} \n Please check directory and input format")
    return False

#Revoke active sessions for the specified account
    #account_object: Python dictionary object that represents a directory account
    #Returns True/False indicating if an account's active sessions were successfully revoked
def revoke_active_sessions(account_object):
    oauth_bearer_token=obtain_oAuth_token_graph_API()
    if not oauth_bearer_token:
        print(f"Failure: Failed to revoke active sessions for account {account_object}. Failed to obtain oAuth Token")
        return False
    response_object=None
    #Locate account's directory object with the Entra ID Directory
    directory_account_object=locate_account_within_directory(account_object,False)
    #If a valid directory object is found, revoke all active sessions for the account
    if directory_account_object:
        response_object=requests.post(url=f"https://graph.microsoft.com/v1.0/users/{directory_account_object.get('userPrincipalName')}/revokeSignInSessions",headers={"Content-Type":"application/json","Authorization":f"Bearer {oauth_bearer_token}"})
    else:
        print(f"Failed to revoke sessions for the input account. Issue with input format OR account: '{account_object.get('Account')}' does NOT exist with Entra ID directory")
        return False
    #Check response codes to validate account's active sessions were successfully revoked
    if response_object.status_code>=200 and  response_object.status_code<300:
        print(f"Successfully Revoked Active Sessions for Account: {directory_account_object.get('userPrincipalName')}")
        return True
    else:
        print(f"Failed to revoke active sessions. For valid Account: {directory_account_object.get('userPrincipalName')}. HTTP Error Response Code Received")
        print(f"HTTP response code is {response_object.status_code}")
        print(f"REspne body is {response_object.text}")
        return False
#Disable the Entra ID account for the input dictionary object: account_object
    #account_object: Python dictionary object that represents a directory account
    #Returns True/False indicating if the Entra ID account for the input object was successfully disabled
def disable_Entra_Account(account_object):
    oauth_bearer_token=obtain_oAuth_token_graph_API()
    if not oauth_bearer_token:
        print(f"Failure: Failed to disable Entra ID account for {account_object}: Failed to obtain oAuth Token")
        return False
    #Disable the Entra ID account
    response_object=None
    #Locate input account_object's directory object with the Entra ID Directory
    directory_account_object=locate_account_within_directory(account_object,False)
    #Valid account found. Attempt to disable the Entra account
    if directory_account_object:
        response_object=requests.patch(url=f"https://graph.microsoft.com/v1.0/users/{directory_account_object.get('userPrincipalName')}",headers={"Authorization":f"Bearer {oauth_bearer_token}","Content-Type":"application/json"},data=json.dumps({"accountEnabled":False}))
    #No valid Entra ID account found. Return False
    else:
        print(f"Failed to disable the input account. Issue with input format OR account: {account_object} does NOT exist within the Entra ID directory")
        entra_Id_Action_Output_Report(account_object,datetime.datetime(2025,4,27).now(),"Disable Entra Account","Failure",f"Failed to disable the input account: {account_object} Input account is NOT a valid Entra ID account")
        return False
    
    #Validate the response code to see if account was successfully disabled
    if response_object.status_code==204:
        print(f"Successfully Disabled Entra Account: {directory_account_object.get('userPrincipalName')}")
        entra_Id_Action_Output_Report(directory_account_object,datetime.datetime(2025,4,27).now(),"Disable Entra Account","Success","None")
        return True
    else:
        print(f"Failed to disable the Entra account: {directory_account_object.get('userPrincipalName')} Possible network or API permissions issue")
        entra_Id_Action_Output_Report(directory_account_object,datetime.datetime(2025,4,27).now(),"Disable Entra Account","Failure",f"Failed to disable the Entra account: {directory_account_object.get('userPrincipalName')} Possible network or API permissions issue")
        return False

#Retrieves the Entra ID sign in logs over past x number days for the input Entra ID account
    #account_object: Python dictionary object that represents a directory account
    #number_of_days: integer representing the number of days in the past to retrieve sign in logs
    #only_interactive: Boolean specifying if only interactive sign-in logs should be retrieved
    #Returns True/False indicating if sign-in logs were successfully retrieved
def retrieve_Sign_In_Logs_For_Account_EntraID(account_object,number_of_days,only_interactive):
    oauth_bearer_token=obtain_oAuth_token_graph_API()
    if not oauth_bearer_token:
        print(f"Failure: Failed to retrieve Entra Sign-In logs for account {account_object}: Failed to obtain oAuth Token")
        return False
    #Retreive Sign-In logs over x number of days for input Entra ID account
    directory_account=locate_account_within_directory(account_object,False)
    response_object=None
    if  directory_account and  only_interactive:
        response_object=requests.get(url="https://graph.microsoft.com/v1.0/auditLogs/signIns",headers={"Authorization":f"Bearer {oauth_bearer_token}"},params={"$filter":"createdDateTime ge 2025-04-01T00:00:00Z and isInteractive eq true and userPrincipalName eq {directory_account.get('userPrincipalName')}"})
    elif directory_account and not only_interactive:
        response_object=requests.get(url="https://graph.microsoft.com/v1.0/auditLogs/signIns",headers={"Authorization":f"Bearer {oauth_bearer_token}"},params={"$filter":"createdDateTime ge 2025-04-01T00:00:00Z and userPrincipalName eq {directory_account.get('userPrincipalName')}"})
    else:
        print(f"Failed to retrieve Sign-In logs for the input account. Issue with input format OR account: '{account_object.get('Account')}' does NOT exist with Entra ID directory")
        return False
    
    #Validate response code
    if response_object and response_object.status_code ==200:
        print(f"Successfully retrieved sign in logs for account: {account_object.get('Account')}")
        list_of_signInLogs_for_user=response_object.json().get('value')
        constructued_output_non_raw_string=f"/Users/josephbrennan/githubProjects/SOC_Automations/outputfiles/retrieve_signInLogs_Account_{directory_account.get('userPrincipalName')}.jsonl"
        with open(return_raw_string(constructued_output_non_raw_string),'w') as file_obj:
            for json_log in list_of_signInLogs_for_user:
                file_obj.write(json.dumps(json_log))
                file_obj.write('\n')
        print(f"Successfully wrote Sign-In logs over past {number_of_days} days for account {directory_account.get('userPrincipalName')} to file: {constructued_output_non_raw_string}")
        return True
    else:
        print(f"Failed to retrieve Sign-In logs for  Entra account: {directory_account.get('userPrincipalName')}. Possible network or API permissions issue")
        print(f"The response code from the server is {response_object.status_code}")
        print(f"The response body from the server is {response_object.text}")
        return False
    
#Returns the raw string version of input non_raw_string
     #non_raw_string: A python string that is not a raw string
     #Returns the raw string version of non_raw_string
def return_raw_string(non_raw_string):
    return r'{}'.format(non_raw_string)

#Raise SNOW INC ticket requesting a block of IP Addresses at all FW environments
    #SNOWDomain: Subdomain providing your org's unique identifier in the SNOW enviroment EX: yourorgdomain.service-now.com
    #dictionary_of_FW_Enviroments_And_SNOW_Groups: Dictionary where each key represents a Firewall enviroment where an INC must be raised. Value is a list of attributes needed to raise SNOW INC in that enviroment
    #Returns True/False indicating if SNOW INC successfully raised in each FW enviroment
def raise_INC_SNOW_Ticket_FWBlock_of_IPAddresses(SNOWDomain,list_of_IPs_for_blocking,dictionary_of_FW_Enviroments_And_SNOW_Groups):
    #Obtain Bearer Token
    bearer_token=obtain_oAuth_token_SNOW_Table_API(SNOWDomain)
    if not bearer_token:
        print("Failure: Failed to raise SNOW ticket to block IP Addresses because oAuth token failed to be returned")
        return False
    #Intalize dictionary of FW enviroments
    dictionary_of_FW_Enviroments_And_SNOW_Groups={"dc_1FW":["Firewallteam","category","subcategory"]}
   
    #Create SNOW INC tickets in each FW Enviroment
    inc_endpoint=f"https://{SNOWDomain}.service-now.com/api/now/table/incident"
    block_ticket_raised_in_each_enviroment=[]
    for fw_enviroment in dictionary_of_FW_Enviroments_And_SNOW_Groups.keys():
        dict_for_raisingTicket={}
        dict_for_raisingTicket['description']=f"Please block the attached IP addresses - {fw_enviroment}"
        dict_for_raisingTicket['short_description']=f"Block IPs - {fw_enviroment}"
        #dict_for_raisingTicket['requested_by']=current_account.name
        #dict_for_raisingTicket['requested_by_email']=current_account.mail
        dict_for_raisingTicket['active']=True
        #CallerID identifies who is raising the incident (like their SNOW sys_user id... Need API integration here... Caller ID isn't required
        #dict_for_raisingTicket['caller_id']=""
        dict_for_raisingTicket['urgency']=3
        dict_for_raisingTicket['impact']=3
        dict_for_raisingTicket['severity']=3
        dict_for_raisingTicket['state']=1
        dict_for_raisingTicket['priority']=3
        dict_for_raisingTicket['assignment_group']=dictionary_of_FW_Enviroments_And_SNOW_Groups.get(fw_enviroment)[0]
        dict_for_raisingTicket['category']=dictionary_of_FW_Enviroments_And_SNOW_Groups.get(fw_enviroment)[1]
        dict_for_raisingTicket['subcategory']=dictionary_of_FW_Enviroments_And_SNOW_Groups.get(fw_enviroment)[2]
        dict_for_raisingTicket['state']='draft'
        response_to_raise_FW_Block_Tickets=requests.post(url=inc_endpoint,headers={"Authorization":f"Bearer {bearer_token}","accept":"application/json","Content-Type":"application/json"},data=json.dumps(dict_for_raisingTicket))
        if response_to_raise_FW_Block_Tickets.status_code==201:
            print(f"Success: The request to raise an INC ticket to IPs at the Firewalls was successful")
            block_ticket_raised_in_each_enviroment.append(True)
        else:
            print(f"Failure: The request to raise an INC ticket to block IPs at firewall enviroment {fw_enviroment} was unsuccessful")
            print(f"The server response code to block IPs at firewall enviroment {fw_enviroment} is  {response_to_raise_FW_Block_Tickets.status_code}")
            block_ticket_raised_in_each_enviroment.append(False)
    if False not in block_ticket_raised_in_each_enviroment:
        print("Success: SNOW INC Tickets successfully raised in each FW enviroment")
        return True
    else:
        print("Failure: SNOW INC Tickets NOT successfully raised in each FW enviroment")
        return False
    #Sys_ fields in SNOW are generated by the SNOW table backend system so I don't need to populate

#Raise SNOW INC ticket requesting password rotation of specificed account
    #SNOWDomain: Subdomain providing your org's unique identifier in the SNOW enviroment EX: yourorgdomain.service-now.com
    #account_object: Python dictionary representing an account object
    #map_of_directories_and_SNOW_Groups: Dictionary where each key is a directory environment and each value is a list of attributes needed to raise SNOW INC for password rotation in that environment
    #Returns True/False indicating if SNOW INC successfully raised in each directory enviroment
def raise_INC_SNOW_Ticket_Ticket_Rotate_Account_Password(SNOW_Domain,account_object,map_of_directories_and_SNOW_Groups):
    #Validate input account exists within Entra ID Directory
    directory_account=locate_account_within_directory(account_object,False)
    if not directory_account:
        print(f"Failed to raise password rotation SNOW INC for the input account. Issue with input format OR account: {account_object} does NOT exist within Entra ID Directory")
        return False
    #Obtain oAuth Token
    bearer_token=obtain_oAuth_token_SNOW_Table_API(SNOW_Domain)
    if not bearer_token:
        print(f"Failed to raise INC SNOW Ticket to rotate account PW. Failed to obtain oAuth Token")
        return False
    
    map_of_directories_and_SNOW_Groups={"entraid":["PWChangeFolks","category","subcategory"]}
    
    list_of_Password_Rotations_Successfully_Raised_In_Each_Directory_Enviroment=[]
    inc_endpoint=f"https://{SNOWDomain}.service-now.com/api/now/table/incident"
    for directory in map_of_directories_and_SNOW_Groups.keys():
        map_of_request_body={}
        map_of_request_body['description']=f"Password Rotation: Please rotate the password for account: {directory_account.get('userPrincipalName')}"
        map_of_request_body['short_description']="Password Rotation"
        #map_of_request_body['requested_by']=current_account.name
        #map_of_request_body['requested_by_email']=current_account.mail
        map_of_request_body['active']=True
        #CallerID identifies who is raising the incident (like their SNOW sys_user id... Need API integration here... Caller ID isn't required
        #dict_for_raisingTicket['caller_id']=""
        map_of_request_body['urgency']=3
        map_of_request_body['impact']=3
        map_of_request_body['severity']=3
        map_of_request_body['state']=1
        map_of_request_body['priority']=3
        map_of_request_body['assignment_group']=map_of_directories_and_SNOW_Groups.get(directory)[0]
        map_of_request_body['category']=map_of_directories_and_SNOW_Groups.get(directory)[1]
        map_of_request_body['subcategory']=map_of_directories_and_SNOW_Groups.get(directory)[2]
        map_of_request_body['state']='draft'
        resonse_object_for_raising_INC_request=requests.post(url=inc_endpoint,headers={"Accept":"application/json","Content-Type":"application/json","Authorization":f"Bearer {bearer_token}"},data=json.dumps(map_of_request_body))
        if resonse_object_for_raising_INC_request.status_code==201:
            print(f"Success: Successfully raised SNOW INC to rotate account password for account {directory_account.get('userPrincipalName')} in directory: {directory}")
            list_of_Password_Rotations_Successfully_Raised_In_Each_Directory_Enviroment.append(True)
        else:
            print(f"Failure: Failed to raise SNOW INC to rotate account password for account {directory_account.get('userPrincipalName')} in directory:  {directory}")
            print(f"The response code for the failed request to raise SNOW INC is : {resonse_object_for_raising_INC_request.status_code}")
            list_of_Password_Rotations_Successfully_Raised_In_Each_Directory_Enviroment.append(False)
    if False not in list_of_Password_Rotations_Successfully_Raised_In_Each_Directory_Enviroment:
        print(f"Success: SNOW INC raised for password rotation for account: {directory_account.get('userPrincipalName')} within each directory enviroment")
        return True
    else:
        print("Failure: SNOW INC Tickets NOT successfully raised in each directory enviroment")
        return False
#Triggers an MDE AV scan on the specificed host
    #host_id: String Unique MDE identifier for the host
    #scan_type: String that specifies the type of the scan that should be triggered.
         #Option 1: Quick Scan
         #Option 2: Full scan
    #input_comment: String message that analyst inputs when triggering the MDE scan
    #Returns True/False indicating if MDE scan successfully triggered
def trigger_MDE_AV_Scan(host_id,scan_type,input_comment):
    #Obtain oAuth Bearer Token
    bearer_token=obtain_oAuth_token_MDE_API()
    if not bearer_token:
        print(f"Failure: Failed to trigger MDE AV scan on {host_id}. Failed to obtain oAuth Token")
        return False
    #Check the MDE scan type
    if scan_type.lower()[0]=='q':
        scan_type="Quick"
    elif scan_type.lower()[0]=='f':
        scan_type="Full"
    #Trigger the AV Scan
    response_from_request_to_trigger_scan=requests.post(url=f"https://api.security.microsoft.com/api/machines/{host_id}/runAntiVirusScan",headers={"Authorization":f"Bearer {bearer_token}","Content-Type":"application/json"},data=json.dumps({"Comment":input_comment,"ScanType":scan_type}))
    #Check the output from the scan
    if response_from_request_to_trigger_scan.status_code==201:
        print(f"Successfully trigger AV scan for host: {host_id}")
        return True
    else:
        print(f"The response code from the server is {response_from_request_to_trigger_scan.status_code}")
        print(f"The response body from the server is {response_from_request_to_trigger_scan.text}")
        print(f"Failed to trigger AV scan for host: {host_id}")
        return False

#Revokes all Entra ID MFA Methods enrolled for an Entra ID account
    #account_object: Python dictionary representing an Entra ID account
    #Returns True/False indicating if all MFA methods were revoked for an account
def revoke_MFA_Methods(account_object):
    #Obtain oAuth Bearer Token
    bearer_token=obtain_oAuth_token_graph_API()
    if not bearer_token:
        print(f"Failure: Failed to revoke account's MFA methods: Failed to obtain oAuth Token")
    
    #Identify valid Entra ID account for input object
    valid_account=locate_account_within_directory(account_object,False)
    if not valid_account:
        print(f"Please check input account format. Failed to identify a valid account within Entra ID for account {account_object}")
        return False
    
    #Obtain all authentication methods enrolled for the Entra ID account
    response_object_for_list_of_authentication_methods=requests.get(url=f"https://graph.microsoft.com/v1.0/users/{valid_account.get('userPrincipalName')}/authentication/methods",headers={"Authorization":f"Bearer {bearer_token}"})
    if response_object_for_list_of_authentication_methods.status_code==200:
        list_of_authentication_mechanisms_for_Entra_ID_account=response_object_for_list_of_authentication_methods.json().get('value')
    else:
        print(f"Failed to retrieve the MFA methods for account: {valid_account.get('userPrincipalName')} : Possible API Permissions issue or network issue")
        return False
    #Attempt to revoke each MFA method
    list_of_outcomes=[]
    for authentication_dictioanry in list_of_authentication_mechanisms_for_Entra_ID_account:
        #Revoke Email MFA method
        if "#microsoft.graph.emailAuthenticationMethod".lower() == authentication_dictioanry.get('@odata.type').lower():
            list_of_outcomes.append(revoke_mail_MFA_method(valid_account))
        #Revoke FIDO MFA method
        elif "#microsoft.graph.fido2AuthenticationMethod".lower() == authentication_dictioanry.get('@odata.type').lower():
            list_of_outcomes.append(revoke_fido_MFA_method(valid_account,authentication_dictioanry))
        #Revoke Microsoft Authenticator MFA method
        elif "#microsoft.graph.microsoftAuthenticatorAuthenticationMethod".lower() == authentication_dictioanry.get('@odata.type').lower():
            list_of_outcomes.append(revoke_MS_Authenticator_App_MFA_method(valid_account,authentication_dictioanry))
        #Revoke Phone MFA method
        elif "#microsoft.graph.phoneAuthenticationMethod".lower() == authentication_dictioanry.get('@odata.type').lower():
            list_of_outcomes.append(revoke_phone_MFA_method(valid_account,authentication_dictioanry))
        #Revoke platform credentials MFA Method
        elif "#microsoft.graph.platformCredentialAuthenticationMethod".lower()==authentication_dictioanry.get('@odata.type').lower():
            list_of_outcomes.append(revoke_platform_MFA_method(valid_account,authentication_dictioanry))
        #Revoke Software token MFA method
        elif "#microsoft.graph.softwareOathAuthenticationMethod".lower() == authentication_dictioanry.get('@odata.type').lower():
            list_of_outcomes.append(revoke_oAth_MFA_method(valid_account,authentication_dictioanry))
        #Revoke temporaryAccessPass MFA Method
        elif "microsoft.graph.temporaryAccessPassAuthenticationMethod".lower()==authentication_dictioanry.get('@odata.type').lower():
            list_of_outcomes.append.append(revoke_temporary_Access_Path_MFA_method(valid_account,authentication_dictioanry))
        elif "#microsoft.graph.windowsHelloForBusinessAuthenticationMethod".lower() == authentication_dictioanry.get('@odata.type').lower():
            list_of_outcomes.append(revoke_Windows_Hello_MFA_Method(valid_account,authentication_dictioanry))
    #Validate revoking all MFA methods was successful
    if False in set(list_of_outcomes):
        print(f"Failure: Failed to revoke all MFA methods for account {valid_account.get('userPrincipalName')}")
    else:
        print(f"Success: All MFA methods successfully revoked for account {valid_account.get('userPrincipalName')}")
        
def entra_Id_Action_Output_Report(directory_object,timestamp,action_taken,action_outcome,error):
    output_dict={}
    if "userPrincipalName" in directory_object.keys():
        output_dict['Account']=directory_object.get('userPrincipalName')
    else:
        output_dict['Account']=directory_object
    output_dict["Action"]=action_taken
    output_dict["Outcome"]=action_outcome
    output_dict["Error"]=error
    with open('/Users/josephbrennan/githubProjects/SOC_Automations/outputfiles/output_report_of_workflow_run.json','w') as file_obj:
        file_obj.write(json.dumps(output_dict))
        file_obj.write('\n')

def revoke_mail_MFA_method(directory_object):
    oath_token=obtain_oAuth_token_graph_API()
    if not oath_token:
        print("Failure: Failed to revoke email/mail MFA Method: Failed to obtain oAuth Token")
        return False
    #Attempt to revoke email MFA method
    response_to_revoke_email_MFA_method=requests.delete(url=f"https://graph.microsoft.com/v1.0/users/{directory_object.get('userPrincipalName')}/authentication/emailMethods/3ddfcfc8-9383-446f-83cc-3ab9be4be18f",headers={"Authorization":f"Bearer {oath_token}"})
    #Validate MFA method successfully revoked
    if response_to_revoke_email_MFA_method.status_code==204:
        print(f"Success: Revoked email MFA method for account: {directory_object.get('userPrincipalName')}")
        return True
    else:
       print(f"Failure: Failed to revoke email MFA method for account: {directory_object.get('userPrincipalName')}")
       return False

def revoke_fido_MFA_method(directory_object,fido_object):
    #Obtain oAuth Token
    oath_token=obtain_oAuth_token_graph_API()
    if not oath_token:
        print(f"Failure: Failed to revoke FIDO MFA Method: Failed to obtain oAuth Token")
        return False
    #Attempt to delete the FIDO MFA Method
    response_to_revoke_fido_MFA_method=requests.delete(url=f"https://graph.microsoft.com/v1.0/users/{directory_object.get('userPrincipalName')}/authentication/fido2Methods/{fido_object.get('id')}",headers={"Authorization":f"Bearer {oath_token}"})
    #Verify the FIDO MFA method was successfully deleted
    if response_to_revoke_fido_MFA_method.status_code== 204:
        print(f"Success: Revoked Fido MFA method: {fido_object.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return True
    else:
       print(f"Failure: Failed to revoke FIDO MFA method:  {fido_object.get('id')} for account: {directory_object.get('userPrincipalName')}")
       return False
    
def revoke_MS_Authenticator_App_MFA_method(directory_object,Authenticator_app_object):
    #Obtain oAuth Token
    oath_token=obtain_oAuth_token_graph_API()
    if not oath_token:
        print(f"Failure: Failed to revoke MS Authenticator Method: Failed to obtain oAuth Token")
        return False
    
    #Attempt to revoke the MS Authenticator MFA Method
    response_to_revoke_MS_Authenticator_APP_MFA_method=requests.delete(url=f"https://graph.microsoft.com/v1.0/users/{directory_object.get('userPrincipalName')}/authentication/microsoftAuthenticatorMethods/{Authenticator_app_object.get('id')}",headers={"Authorization":f"Bearer {oath_token}"})
    #Validate the  MS Authenticator MFA Method successfully revoked
    if response_to_revoke_MS_Authenticator_APP_MFA_method.status_code==204:
        print(f"Success: Revoked MS Authenticator App MFA method: {Authenticator_app_object.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return True
    else:
       print(f"Failure: Failed to revoke MS Authenticator App MFA method: {Authenticator_app_object.get('id')} for account: {directory_object.get('userPrincipalName')}")
       return False
    
def revoke_phone_MFA_method(directory_object,phone_authentication_MFA_Method):
    #Obtain oAuth Token
    oath_token=obtain_oAuth_token_graph_API()
    if not oath_token:
        print(f"Failure: Failed to revoke phone MFA method: Failed to obtain oAuth Token")
        return False
    #Attempt to revoke the phone MFA method
    response_to_revoke_phone_MFA_Method=None
    #Attempt to revoke mobile phone MFA method
    if phone_authentication_MFA_Method.get('phoneType').lower()=="mobile":
        response_to_revoke_phone_MFA_Method=requests.delete(url=f"https://graph.microsoft.com/v1.0/users/{directory_object.get('userPrincipalName')}/authentication/phoneMethods/3179e48a-750b-4051-897c-87b9720928f7",headers={"Authorization":f"Bearer {oath_token}"})
    #Attempt to revoke alternative phone MFA method
    elif phone_authentication_MFA_Method.get('phoneType').lower()=="alternateMobile".lower():
        response_to_revoke_phone_MFA_Method=requests.delete(url=f"https://graph.microsoft.com/v1.0/users/{directory_object.get('userPrincipalName')}/authentication/phoneMethods/b6332ec1-7057-4abe-9331-3d72feddfe41",headers={"Authorization":f"Bearer {oath_token}"})
    #Attempt to revoke office phone MFA method
    elif phone_authentication_MFA_Method.get('phoneType').lower()=="office".lower():
        response_to_revoke_phone_MFA_Method=requests.delete(url=f"https://graph.microsoft.com/v1.0/users/{directory_object.get('userPrincipalName')}/authentication/phoneMethods/e37fc753-ff3b-4958-9484-eaa9425c82bc",headers={"Authorization":f"Bearer {oath_token}"})
    #Verify phone MFA method revocation was successful
    if response_to_revoke_phone_MFA_Method.status_code==204:
        print(f"Success: Revoked phone MFA method: {phone_authentication_MFA_Method.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return True
    else:
        print(f"Failure: Failed to revoke phone MFA method: {phone_authentication_MFA_Method.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return False

def revoke_platform_MFA_method(directory_object,platform_MFA_Object):
    oath_token=obtain_oAuth_token_graph_API()
    if not oath_token:
        print(f"Failure: Failed to revoke platform MFA method: Failed to obtain oAuth Token")
        return False
    
    #Attempt to revoke the Platform MFA Method
    response_object_to_revoke_platform_MFA=requests.delete(url=f"https://graph.microsoft.com/v1.0/users/{directory_object.get('userPrincipalName')}/authentication/platformCredentialMethods/{platform_MFA_Object.get('id')}",headers={"Authorization":f"Bearer {oath_token}"})
    #Validate the attempt to revoke the MFA method was succcessful
    if response_object_to_revoke_platform_MFA.status_code==204:
        print(f"Success: Revoked platform MFA method: {platform_MFA_Object.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return True
    else:
        print(f"Failure: Failed to revoke platform MFA method: {platform_MFA_Object.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return False

def revoke_OATH_MFA_Method(directory_object,oATH_MFA_Object):
    #Obtain oAuth Method
    oath_token=obtain_oAuth_token_graph_API()
    if not oath_token:
        print("Failure: Failed to revoke OATH MFA Method: Failed to obtain oAuth Token")
        return False
    
    #Attempt to revoke the OATH MFA Method
    response_object_to_revoke_OATH_MFA_Method=requests.delete(url="https://graph.microsoft.com/v1.0/users/{directory_object.get('userPrincipalName')}/authentication/softwareOathMethods/{oATH_MFA_Object.get('id')}",headers={"Authorization":f"Bearer {oath_token}"})
    
    #Validate attempt to revoke MFA method was successful
    if response_object_to_revoke_OATH_MFA_Method.status_code==204:
        print(f"Success: Revoked OATH MFA method: {oATH_MFA_Object.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return True
    else:
        print(f"Failure: Failed to revoke OATH MFA method: {directory_object.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return False

def revoke_temporary_Access_Pass_MFA_Method(directory_object,tmp_access_path_MFA_Object):
    #Obtain oAuth Token
    oath_token=obtain_oAuth_token_graph_API()
    if not oath_token:
        print(f"Failure: Failed to revoke temporary MFA Method: Failed to obtain oAuth Token")
        return False
    
    #Attempt to revoke MFA method
    response_to_revoke_tmp_Pass_MFA_Method=requests.delete(url=f"https://graph.microsoft.com/v1.0/users/{directory_object.get('userPrincipalName')}/authentication/temporaryAccessPassMethods/{tmp_access_path_MFA_Object.get('id')}",headers={"Authorization":f"Bearer {oath_token}"})
    #Validate MFA method was successfully revoked
    if response_to_revoke_tmp_Pass_MFA_Method.status_code==204:
        print(f"Success: Revoked Temporary Access Pass MFA Method: {tmp_access_path_MFA_Object.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return True
    else:
        print(f"Failure: Failed to revoke Tmp Access MFA Method: {tmp_access_path_MFA_Object.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return False

def revoked_Windows_Hello_MFA_Method(directory_object,Windows_Hello_MFA_Method):
    #Obtain oAuth Token
    oath_token=obtain_oAuth_token_graph_API()
    if not oath_token:
        print(f"Failure: Failed to revoke Windows Hello MFA Method: Failed to obtain oAuth Token")
        return False
    
    #Request deletion of MFA Method
    windows_hello_deletion_response_objects=requests.delete(url="https://graph.microsoft.com/v1.0/users/{directory_object.get('userPrincipalName')}/authentication/windowsHelloForBusinessMethods/{Windows_Hello_MFA_Method.get('id')}",headers={"Authorization":f"Bearer {oath_token}"})
    
    if windows_hello_deletion_response_objects.status_code==204:
        print(f"Success: Revoked Windows Hello MFA Method: {Windows_Hello_MFA_Method.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return True
    else:
        print(f"Failure: Failed to revoke Windows Hello MFA Method: {Windows_Hello_MFA_Method.get('id')} for account: {directory_object.get('userPrincipalName')}")
        return False

def remove_Entra_Account_From_Enta_Group(account_object,group_id):
    #Obtain oAuth Token and validate valid token returned
    oath_token=obtain_oAuth_token_graph_API()
    if not oath_token:
        print(f"Failure: Failed to remove {account_object} from {group_id}: Failed to obtain oAuth Token")
        return False
    #Located a valid Entra ID account. Return False if no valid account found
    directory_account=locate_account_within_directory(account_object,False)
    if not directory_account:
        return False
    if not re.search(r'\w{8}\-\w{4}\-\w{4}',directory_account.get('id')):
        print("Directory account's object value isn't properly formatted. API call would fail")
        return False
    
    #Attempt to remove the account from the group
    response_object_to_remove_user_from_group=requests.delete(url=f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/{directory_account.get('id')}/$ref",headers={"Authorization":f"Bearer {oath_token}"})
    #Validate user successfully removed from Entra ID
    if response_object_to_remove_user_from_group.status_code==204:
        print(f"Success: Removed account {directory_account.get('id')} from: group {group_id}")
        return True
    elif response_object_to_remove_user_from_group.status_code==404:
        print(f"Failure: Failed to remove account {directory_account.get('id')} from: group {group_id}. Group does not exist OR Object not a member of the group")
        return False
    else:
        print(f"Failure: Failed to remove account {directory_account.get('id')} from group {group_id}")
        return False

def obtain_oAuth_token_graph_API():
    #Obtain oAuth Token
    load_dotenv()
    read_in_client_id=os.getenv("Graph_API_Client_Id")
    read_in_client_secret=os.getenv("Graph_API_Client_Secret")
    oAuth_post_request_body={"grant_type":"client_credentials","resource":"https://graph.microsoft.com","client_id":read_in_client_id,"client_secret":read_in_client_secret}
    oauth_response_object=requests.post(url="https://login.microsoftonline.com/8e1d2836-0590-44ba-a737-5761471408d8/oauth2/token",data=oAuth_post_request_body)
    oath_token=None
    if oauth_response_object.status_code>=200 and oauth_response_object.status_code<300:
        return oauth_response_object.json().get('access_token')
    else:
        print(f"Failed to retrieve oAuth Bearer Token. Received response code was {oauth_response_object.status_code}")
        return False

def obtain_oAuth_token_MDE_API():
    load_dotenv()
    read_in_client_id=os.getenv("Graph_API_Client_Id")
    read_in_client_secret=os.getenv("Graph_API_Client_Secret")
    post_request_body={'grant_type':"client_credentials","resource":"https://api.security.microsoft.com","client_id":read_in_client_id,"client_secret":read_in_client_secret}
    bearer_token=None
    oauth_request_response_object=requests.post(url="https://login.microsoftonline.com/8e1d2836-0590-44ba-a737-5761471408d8/oauth2/token",data=post_request_body)
    if oauth_request_response_object.status_code>=200 and oauth_request_response_object.status_code<300:
        return oauth_request_response_object.json().get('access_token')
    else:
        print(f"Failed to retrieve oAuth Bearer Token. Received response code was {response_object.status_code}")
        return False


def obtain_oAuth_token_SNOW_Table_API(SNOWDomain):
    #Obtain oAuth Token
    Read_In_SNOW_Client_ID=""
    SNOW_Client_Secret=""
    oAuthEndpoint=f"https://{SNOWDomain}.service-now.com/oauth_token.do"
    post_request_body_for_token={"client_id":Read_In_SNOW_Client_ID,"client_secret":SNOW_Client_Secret,"grant_type":"client_credentials"}
    response_object=requests.post(url=oAuthEndpoint,data=post_request_body_for_token)
    bearer_token=None
    print(f"OAuthRequest response code for Bearer Token: {response_object.status_code}")
    if response_object.status_code>=200 and response_object.status_code<300:
        return response_object.json().get('access_token')
    else:
        print(f"Failed to retrieve oAuth Bearer Token. Received response code was {response_object.status_code}")
        return False

def parse_input_user_format(file_format,path_to_file):
    print("Attempting to read in input account objects")
    list_of_json_objects=[]
    #Parse CSV input file
    if file_format.lower()=="csv":
        #read in Pandas DF
        input_df=pd.read_csv(return_raw_string(path_to_file))
        #Valid Account field exists within the input CSV file
        if "Account" not in input_df.columns:
            print(f"Failure: Failed to read in input accounts because invalid input file format: No 'Account' field within the input csv")
            return False
        #Create list of dictionary objects that contain Account field
        for account_str in input_df['Account'].to_list():
            new_dict_object={"Account":account_str}
            list_of_json_objects.append(new_dict_object)
        print("Success: Successfully read in input account objects from CSV file")
        return list_of_json_objects
    #Parse list of JSON objects where each object is a account identifer
    elif file_format.lower()=="json":
        #Read in the json file
        with open(return_raw_string(path_to_file),'r') as file_obj:
            list_of_json_objects=json.load(file_obj)
        #Validate input format
        for dictionary in list_of_json_objects:
            if 'Account' not in dictionary.keys():
                print("Failed to read in input accounts because invalid input file format: No 'Account' field within the input JSON list of objects")
                return False
        #Return list of Python dictionaries
        print("Success: Successfully read in input account objects from JSON file")
        return list_of_json_objects
    #Parse ndJSON or JSONL file
    elif file_format.lower()=="ndjson" or file_format.lower()=="jsonl":
        #Read in the input file:
        with open(return_raw_string(path_to_file),'r') as file_obj:
            list_of_json_objects=file_obj.readlines()
        #Convery list of JSON strings into list of Python dictionaries
        list_of_json_objects=[ json.loads(json_str) for json_str in list_of_json_objects]
        #Validate proper input format
        for dictiaonry in list_of_json_objects:
            if 'Account' not in dictiaonry.keys():
                print("Failed to read in input accounts because invalid input file format: No 'Account' field within the input ndJSON or JSONL file")
                return False
        print(f"Success: Successfully read in input account objects from {file_format} file")
        #Return list of Python dictionaries
        return list_of_json_objects


def parse_input_host_format(file_format,path_to_file):
    list_of_host_ids=[]
    print("Attempting to read in input host objects")
    if file_format.lower()=='csv':
        host_df=pd.read_csv(return_raw_string(path_to_file))
        if 'host_id' not in host_df.columns:
            print("Failure: Failed to read in input host_ids because invalid input file format: No 'host_id' field within the input CSV")
            return False
        for host_id in host_df['host_id'].to_list():
            list_of_host_ids.append(host_id.lower().replace(' ',''))
        return list_of_host_ids
    elif file_format.lower()=='json':
        with open(return_raw_string(path_to_file),'r') as file_obj:
            list_of_host_ids=json.load(file_obj)
        for json_object in list_of_host_ids:
            if 'host_id' not in json_object.keys():
                print("Failure: Failed to read in input host_ids because invalid input file format: No 'host_id' field within the input list of JSON objects")
                return False
        return [json_log_object.get('host_id').lower().replace(' ','')  for json_log_object in list_of_host_ids ]
    elif file_format.lower()=='ndjson' or file_format.lower()=='jsonl':
        with open(return_raw_string(path_to_file),'r') as file_obj:
            list_of_host_ids=file_obj.readlines()
        list_of_host_ids=[json.loads(json_str)  for json_str in list_of_host_ids]
        for json_dict in list_of_host_ids:
            if 'host_id' not in json_dict.keys():
                print("Failure: Failed to read in input host_ids because invalid input file format: No 'host_id' field within the input list of JSON objects")
                return False
        return [json_dict.get('host_id') for json_dict in list_of_host_ids]

def parse_input_SNOW_INC(file_format,path_to_file):
    output_dict_of_config_values={}
    #Parse CSV file
    if file_format.lower()=='csv':
        #Extract the ticket type
        snow_input_df=pd.read_csv(return_raw_string(path_to_file))
        if 'ticket_type' not in snow_input_df.columns:
            print('Failed to read in SNOW INC configuration CSV file: Issue with CSV format. \n Validate that ticket_type column appears with the input CSV')
            return False
        output_dict_of_config_values['ticket_type']=snow_input_df['ticket_type'].to_list()[0]
        if 'SNOW_Domain' not in snow_input_df.columns:
            print('Failed to read in SNOW INC configuration CSV file: Issue with CSV format. \n Validate that SNOW_Domain column appears with the input CSV')
            return False
        output_dict_of_config_values['SNOW_Domain']=snow_input_df['SNOW_Domain'].to_list()[0]
        if 'Account' in snow_input_df.columns:
            output_dict_of_config_values['Account']=snow_input_df['Account'].to_list()[0]
        else:
            output_dict_of_config_values['Account']=None
        if 'IPs' in snow_input_df.columns:
            output_dict_of_config_values['IPs']=snow_input_df['IPs'].to_list()[0].replace(' ','').split(',')
    return output_dict_of_config_values
       
