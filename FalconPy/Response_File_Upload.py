#!/usr/bin/env python3
#Please establish an "auth.py" file in the same directory as this script with the "clientid" and "clientsec" variables defined.
#Developed by Don-Swanson-Adobe

####REPLACE THE FOLLOWING EXAMPLE VARIABLES####
f_filepath = "./file.sh"      #Note: './' is 1 directory up from current, '../' is 2 directories up
f_name = "file.sh"            #Name of the file (Including the extension)
f_description = "Description and version number" #Description of the file
f_comment = "comment"           #Comment for Audit Log
###############################################

from falconpy import APIHarnessV2
from auth import *

PAYLOAD = {
    "description": f_description,
    "name": f_name,
    "comments_for_audit_log": f_comment
}
with open(f_filepath, "rb") as upload_file:
    file_upload = [('file', ('MyPutFile', upload_file.read(), 'application/octet-stream'))]

for key, value in cids.items():
    print("\n"+value)
    falcon = APIHarnessV2(client_id=clientid, client_secret=clientsec, member_cid=key)

    response = falcon.command("RTR_CreatePut_Files", data=PAYLOAD, files=file_upload)
    print("Status Code: ",response["status_code"])