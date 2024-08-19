The EDR API is setup as a single Lambda Function with an AWS API Gateway that passes the requests to this function to perform as a poor man's API. Its backend is a DynamoDB which stores the information regarding the latest kernels, sensor date changes, sensor versions, etc. Each .py file in this folder is a separate file within the lambda.  

There is also a health check endpoint that allows a team to call the API to check the health of an individual host programatically. In order to use the Health Check you will need to add the FalconPy Layer to this lambda and provid an SecretManager key with host read permissions.  

You will need to setup a DynamoDB with the following Tables to make full use of this Function, along with setting up the appropriate IAM policies to allow the poor man's API to operate properly:  

Container_Paths  
Latest_Kernel  
Sensor_Versions  
Proposed_Sensor Versions  
Change_Dates #(Dates will be manually added in the format of yyyy-mm-dd. EX: 2023-01-01)  


Note: The "Auth" that is expected to be passed in the header is not treated as a secret. We utilize it to track which teams are using which endpoints and how often. So these Auths are typically in the format of "TEAM1_AUTH", "TEAM2_AUTH", etc.