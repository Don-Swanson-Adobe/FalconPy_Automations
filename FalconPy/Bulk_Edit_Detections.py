#!/usr/bin/env python3
#Please establish an "auth.py" file in the same directory as this script with the "clientid" and "clientsec" variables defined.
#This script was developed to bulk close detections.
#Developed by Don-Swanson-Adobe

#NOTE: There is a bug currently withing the CS API that limits offset to 10000. This script is configured to handle that limitation by sleeping after closing out the first 10k detects then grabbing a new list of detects to close, and repeats until 0 detects remain.
######REPLACE THE FOLLOWING VARIABLES######
uuid = "<REPLACE ME>" #Please replace with your CrowdStrike User's UUID
status = "false_positive" #false_positive, true_positive, ignored, in_progress, new
comment = "<REPLACE ME WITH TICKET NUMBER> - <REPLACE ME WITH A SUMMARY COMMENT>" #Comment to add to the detection
filter="status:'new'+behaviors.cmdline:'<REPLACE ME WITH THE DESIRED COMMANDLINE, MAKE SURE TO ESCAPE ANY QUOTES IN THE COMMANDLINE>'" #filter to search for
###########################################

from falconpy import APIHarnessV2
from auth import *
import time

#Chunky function to split the list into 1000 item chunks
def chunk_list(input_list, chunk_size):
    """Yield successive n-sized chunks from input_list."""
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i:i + chunk_size]

def get_detect_ids(batch_total):
    id_list = []
    offset = 0
    print("\nTotal remaining Detect IDs:")
    while batch_total > 0 and offset < 10000:
        print(batch_total)
        response = falcon.command("QueryDetects",
                                filter=filter,
                                limit=1000,
                                offset=offset,
                                )
        if response["status_code"] != 200:
            print(f"Failed to query detects: {response}")
            exit(1)
        batch_total = batch_total - 1000
        offset = offset + 1000
        id_list.extend(response["body"]["resources"])
    return id_list

def set_detect_status(uuid, status, comment, id_list):
    chunk_total = len(id_list)
    print("\nTotal Remaining Detect Updates in this batch:")
    for chunk in chunk_list(id_list, 1000):
        print(chunk_total)
        BODY = {
            "assigned_to_uuid": uuid,
            "comment": comment,
            "ids": chunk,
        #    "show_in_ui": boolean,
            "status": status,
        }
        response = falcon.command("UpdateDetectsByIdsV2", body=BODY)
        if response["status_code"] != 200:
            print(f"Failed to update detects: {response}")
            exit(1)

        print("Response: ",response["status_code"])
        chunk_total = chunk_total - 1000

#login to the API
falcon = APIHarnessV2(client_id=clientid, client_secret=clientsec)

#Determine total number of results to loop through
response = falcon.command("QueryDetects",
                filter=filter,
                limit=1
                )
if response["status_code"] != 200:
    print(f"Failed to query detects: {response}")
    exit(1)

total = response["body"]["meta"]["pagination"]["total"]

#Loop through and grab all detect IDs
print("Grabbing Detect IDs")
while total > 0:
    id_list = get_detect_ids(total)

    print("Setting Detection Statuses")
    set_detect_status(uuid, status, comment, id_list)
    
    total = total - 10000
    if total > 0:
        print("Sleeping for 30 seconds to allow detections to update and start a new batch of 10k detects.")
        time.sleep(30)