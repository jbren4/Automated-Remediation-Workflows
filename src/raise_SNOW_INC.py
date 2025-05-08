from socautomationfunctions import return_raw_string
from socautomationfunctions import raise_INC_SNOW_Ticket_FWBlock_of_IPAddresses
from socautomationfunctions import raise_INC_SNOW_Ticket_Ticket_Rotate_Account_Password
from socautomationfunctions import parse_input_SNOW_INC
import sys

print('Attempting to read in configuration file specifying type of INC being raised')
#Process input
INC_ticket_config_dict=parse_input_SNOW_INC('csv',return_raw_string('/Users/josephbrennan/githubProjects/SOC_Automations/input_files/raise_SNOW_INC.csv'))

if not INC_ticket_config_dict:
    print("Failed to read in INC SNOW ticket configuration: Please check the input file format")
    sys.exit(0)

#Check whick type of INC is being raised
if INC_ticket_config_dict.get('ticket_type').lower()=='password_rotation':
    print('Attempting to raise Password Rotation INC')
    raise_INC_SNOW_Ticket_Ticket_Rotate_Account_Password(INC_ticket_config_dict.get('SNOW_Domain'),INC_ticket_config_dict,None)
elif INC_ticket_config_dict.get('ticket_type').lower()=='fw_block':
    print('Attempting to raise FW Block of IPs')
    raise_INC_SNOW_Ticket_FWBlock_of_IPAddresses(INC_ticket_config_dict.get('SNOW_Domain'),INC_ticket_config_dict.get('IPs'),None)

print('Workflow complete. Review output report to validate workflow results')

