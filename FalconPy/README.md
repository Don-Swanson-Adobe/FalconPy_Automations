# FalconPy Scripts

Collection of useful python scripts to interact with the API via FalconPy <https://www.falconpy.io/>.  
In order to keep Authentication credentials separate, please edit the auth.py with your CS API Credentials, and keep it in the same directory that you will run the script from.   

## About The Scripts

- Audit_IOAs.py  
  - Outputs a text file with a list of IOA Exclusions and details.  
- Audit_IOCs.py  
  - Outputs a text file with a list of IOC Exclusions and details.  
- Audit_MLEs.py  
  - Outputs a text file with a list of ML Exclusions and details.  
- Audit_SVEs.py  
  - Outputs a text file with a list of SVE Exclusions and details.  
- Bulk_Add_Falcon_Tags.py  
  - Adds a specified Falcon Sensor Tag (AKA Console Tag) to a list of hosts defined by serial number. The source file should be only serial numbers with a separate one on each line.  
- Bulk_Edit_Detections.py  
  - Script to be able to bulk update detections    
- Clone_Prevention_Policy.py  
  - Used for Cloning Prevention Policies from one CID to another.  
- Clone_Update_Policy.py  
  - Used for Cloning Update Policies from one CID to another.  
- Create_Group_Add_To_Prev_Policy.py  
  - Creates a new hostgroup as defined and adds it to the list of provided prevention policies.  
- Create_Group_Add_To_Update_Policy.py  
  - Creates a new hostgroup as defined and adds it to the list of provided update policies.  
- Default_Groups.py  
  - Usefull for new environment setup. Creates a Default set of groups in each CID.  
- Find_Users_In_Child_CIDs.py  
  - For Audit purposes, this script will look for users that are created in Child CIDs. All users should be added at the parent level only.  
- Get_Host_Groups.py  
  - Get a list of Host Groups in each CID.  
- Host_Report.py  
  - Host Report script for audit of hosts with falcon installed.   
- Host_Search.py  
  - Pull basic info for a list of hostnames (separated by a new line). Useful for determining if a large list of hosts has EDR installed and their health.   
- Mass_Assignment_Check.py  
  - Used to verify assignment of new host groups to policies due to the bug where the CS API seems to get overwhelmed with a large amount of create and attach calls and does not perform the assignment of the new group in every CID.  
- Replicate_Falcon_Scripts.py  
  - Replicate a "Falcon Script" into a standrd response script  
- Response_File_Remove.py  
  - Remove an old RTR Response File that has been added to each CID.   
- Response_File_Upload.py  
  - Uploads an RTR Response File to each CID.  
- Response_Script_Remove.py  
  - Remove an old RTR Response Script that has been added to each CID.   
- Response_Script_Upload.py  
  - Uploads an RTR Response Script to each CID.  
- RFM_Report.py  
  - A list of hosts in RFM and basic details about the hosts.  
- RTR_Restart_Sensor.py  
  - An example script to perform RTR Commands via FalconPy. This example pushes the remote tcpdump bash script and starts it via systemd-run so that it launches in it's own environment and can restart the Falcon Sensor without being killed when the sensor is stopped.   
- Serial_Search.py  
  - Pull basic info for a list of serials (separated by a new line). Useful for determining if a large list of hosts has EDR installed and their health.  