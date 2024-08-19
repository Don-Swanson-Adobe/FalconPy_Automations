# Automation Lambdas

Collection of Lambdas that run the core infrastructure of the EDR Ops Team's Automation.

## About The Scripts

- EDR_API  
  - This Folder contains the files that make up the Lambda Function that constitutes the EDR API.  
- ArtifactoryInstallerUpdater.py  
  - Will pull the installer files for the current DEV/PRD Sensor versions and upload them to Artifactory.  
- FalconBot-EDR_End.py  
  - The Backend of FalconBot that retrieves host data from the CrowdStrike API, formats it, and sends the response to Slack.  
- FalconBot-Slack_End.py  
  - The Frontend for All FalconBot Commands in Slack. This accepts the Slack commands, validates their source, extracts data, then passes it along to the correct Backend Lambda for further processing.  
- Intel_Downloads.py  
  - Automation that pulls the Daily CrowdStrike Intel Report and pushes it to Slack and Via Email to a Distro List.  
- Pick_Next_Sensor_Version.py  
  - Runs prior to an established Sensor Version Change Date to pick the next recommended sensor version.  
- Sensor_Version_Changer.py  
  - On the established Sensor Version Change Date, it will change the Sensor Update policies to the proposed versions.  
- Update_Supported_Kernels_List_Sorted.py  
  - Runs Daily to update the Wiki supported Kernels listing.



# Layers:
Note, you will need to create a Lamda Layer Package for the following python projects to be uploaded (Insutructions in the attached PDF):  
falconpy
natsort
packaging_version
repomd
tabulate