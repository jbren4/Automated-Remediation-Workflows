import requests
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
    account_already_enriched=False
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
        elif  enabled_account.get(unique_account_identifier_attribute)!=None and enabled_account.get(unique_account_identifier_attribute).lower().replace(' ','')==attribute_that_will_enrich_the_event_with.lower().replace(' ','') and log_type=="JSON":
            account_already_enriched=True
            if enabled_account.get('userPrincipalName'):
                log_object[f'UPN']=enabled_account.get('userPrincipalName')
            else:
                log_object[f'UPN']="Not Found"
            if enabled_account.get('userType'):
                log_object[f'User_Type']=enabled_account.get('userType')
            else:
                log_object[f'User_Type']="Not Found"
            if enabled_account.get('createdDateTime'):
                log_object[f'Account_Creation_Date']=enabled_account.get('createdDateTime')
            else:
                log_object[f'Account_Creation_Date']="Not Found"
            if enabled_account.get('lastPasswordChangeDateTime'):
                log_object[f'Last_Password_Change_TimeStamp']=enabled_account.get('lastPasswordChangeDateTime')
            else:
                log_object[f'Last_Password_Change_TimeStamp']="Not Found"
            if enabled_account.get('jobTitle'):
                log_object[f'Job_Title']=enabled_account.get('jobTitle')
            else:
                log_object[f'Job_Title']="Not Found"
            if enabled_account.get('companyName'):
                log_object[f'Company_Name']=enabled_account.get('companyName')
            else:
                log_object[f'Company_Name']="Not Found"
            if enabled_account.get('department'):
                log_object[f'Department']=enabled_account.get('department')
            else:
                log_object[f'Department']="Not Found"
            if enabled_account.get('employeeId'):
                log_object[f'employee_Id']=enabled_account.get('employeeId')
            else:
                log_object[f'employee_Id']="Not Found"
            if enabled_account.get('officeLocation'):
                log_object[f'Office_Location']=enabled_account.get('officeLocation')
            else:
                log_object[f'Office_Location']="Not Found"
            if enabled_account.get('state'):
                log_object[f'Region']=enabled_account.get('state')
            else:
                log_object[f'Region']="Not Found"
            if  enabled_account.get('postalCode'):
                log_object[f'Postal_Code']=enabled_account.get('postalCode')
            else:
                log_object[f'Postal_Code']="Not Found"
            if enabled_account.get('country'):
                log_object[f'Country']=enabled_account.get('country')
            else:
                log_object[f'Country']="Not Found"
            if enabled_account.get('mail'):
                log_object[f'Email']=enabled_account.get('mail')
            else:
                log_object[f'Email']="Not Found"
            if enabled_account.get('mailNickname'):
                log_object[f'Mail_Nickname']=enabled_account.get('mailNickname')
            else:
                log_object[f'Mail_Nickname']="Not Found"
            manager_response_object=requests.get(url=f"https://graph.microsoft.com/v1.0/users/{enabled_account.get('userPrincipalName')}/manager",headers={"authorization":f"Bearer {bearer_token_for_graph_api_requests}"})
            if manager_response_object.status_code==200:
                log_object[f'Manager']=manager_response_object.json().get('userPrincipalName')
            else:
                log_object[f'Manager']="Not Found"
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
    #Account field within JSON log wasn't found within an account within the cloud directory. Thus indicate account not found
    elif not account_already_enriched  and log_type=="JSON":
        log_object[f'UPN']="Account not found within Entra ID"
        log_object[f'User_Type']="Account not found within Entra ID"
        log_object[f'Account_Creation_Date']="Account not found within Entra ID"
        log_object[f'Last_Password_Change_TimeStamp']="Account not found within Entra ID"
        log_object[f'Job_Title']="Account not found within Entra ID"
        log_object[f'Company_Name']="Account not found within Entra ID"
        log_object[f'Department']="Account not found within Entra ID"
        log_object[f'employee_Id']="Account not found within Entra ID"
        log_object[f'Office_Location']="Account not found within Entra ID"
        log_object[f'Region']="Account not found within Entra ID"
        log_object[f'Postal_Code']="Account not found within Entra ID"
        log_object[f'Country']="Account not found within Entra ID"
        log_object[f'Email']="Account not found within Entra ID"
        log_object[f'Mail_Nickname']="Account not found within Entra ID"
        log_object[f'Manager']="Account not found within Entra ID"
