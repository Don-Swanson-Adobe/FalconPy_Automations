#!/usr/bin/env python3
#Please establish an "auth.py" file in the same directory as this script with the "clientid" and "clientsec" variables defined.
#Developed by Don-Swanson-Adobe

####REPLACE THE FOLLOWING EXAMPLE VARIABLES####
f_names = ["file1.exe","file2.sh"] #List of file names to remove
###############################################

from falconpy import APIHarnessV2
from auth import *

for key, value in cids.items():
    print("\n"+value)
    falcon = APIHarnessV2(client_id=clientid, client_secret=clientsec, member_cid=key)
    for name in f_names:
        #Find Script
        response = falcon.command("RTR_ListPut_Files",filter="name:'"+name+"'")
        if response["body"]["resources"] == []:
            print("Script not found")
            continue
        id = response["body"]["resources"][0]
        print("Script ID: ",id)
        #Remove Script
        response = falcon.command("RTR_DeletePut_Files", ids=id)
        print("Status Code: ",response["status_code"])