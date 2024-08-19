#!/usr/bin/env python3
#Please establish an "auth.py" file in the same directory as this script with the "clientid" and "clientsec" variables defined.
#This script was intended to replicate selected Falcon Scripts to be usable by all RTR Active Responders in each CID
#Developed by Don-Swanson-Adobe

####REPLACE THE FOLLOWING EXAMPLE VARIABLES####
f_comment = "COMMENT"       #Comment for Audit Log
f_permission = "public"     #private: usable by only the user who uploaded it
                            #group: usable by all RTR Admins
                            #public: usable by all active-responders and RTR admins
list_of_script_names = ["Script1", "Script2", "Script3"] #List of script names to replicate
###############################################

from falconpy import APIHarnessV2
from auth import *
from datetime import datetime

update_time = datetime.utcnow().isoformat(timespec='minutes')

for name in list_of_script_names:
    #Login and Find Script ID
    falcon = APIHarnessV2(client_id=clientid, client_secret=clientsec)
    response = falcon.command("RTR_ListFalconScripts",filter="name:'"+name+"'")
    id_list = response["body"]["resources"][0]

    #Get Script Details
    response = falcon.command("RTR_GetFalconScripts", ids=id_list)
    content = response["body"]["resources"][0]["content"]
    name = response["body"]["resources"][0]["name"]
    description = "Cloned from Falcon Scripts on "+update_time+";  "+response["body"]["resources"][0]["description"] + " " + response["body"]["resources"][0]["use_case"]
    platform = response["body"]["resources"][0]["platform"]

    #Format Payload
    PAYLOAD = {
        "description": description,
        "name": name,
        "comments_for_audit_log": f_comment,
        "permission_type": f_permission,
        "platform": [platform],
        "content": content
    }

    #Replicate Script to all CIDs
    for key, value in cids.items():
        print("\n"+value)
        falcon = APIHarnessV2(client_id=clientid, client_secret=clientsec, member_cid=key)
        response = falcon.command("RTR_CreateScripts", data=PAYLOAD, files={"content":content})
        print(response)
        print("Status Code: ",response["status_code"])