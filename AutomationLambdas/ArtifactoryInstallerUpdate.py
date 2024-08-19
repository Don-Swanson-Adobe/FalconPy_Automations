#This lambda automation is designed to pull down the latest Sensor Installers from the Falcon API and upload them to an Artifactory server
#Please see the attached PDF for how to setup Secrets Manager and the IAM role for these Lambda function
#The attached PDF Also includes instructions on how to setup and add an AWS Layer to this Lambda function to use FalconPy
#Required Layers for this Function: FalconPy
#You will also need to increase the Lambda Timeout to 15 minutes, the memory to 1024MB, and the ephemeral storage to 2048MB
#Please be sure to look carefully through this script as there may be locations you should update/edit yout Artifactory paths or AWS Secret IDs


##### REPLACE THE FOLLOWING VALUES#####
#Global Vars
af_base = "https://artifactoryserver.somecompany.com/artifactory/" #Replace with your base URL for your Artifactory Server
slackhook = "https://hooks.slack.com/services/ABCDEFG/123456789012345678901234567890" #Replace with the webhook URL To recieve Slack Notifications
pols = { #Replace with the policy IDs for your environments
    "windows_dev":"123456789012345678901234567890", 
    "mac_dev":"123456789012345678901234567890", 
    "linux_dev":"123456789012345678901234567890", 
    "windows_prd":"123456789012345678901234567890", 
    "mac_prd":"123456789012345678901234567890", 
    "linux_prd":"123456789012345678901234567890"}
environ =["PRD","DEV"]
afusername = "artifactory_user_name" #Replace with the username for your Artifactory Server
EDR_API_URL = "https://AWS_API_GATEWAY.amazonaws.com"
#######################################

#!/usr/bin/env python3
from falconpy import APIHarness
from falconpy import SensorDownload
import requests
import json
import boto3
import time
from multiprocessing import Process, Pipe

#############################################
## Script will pull the PRD/DEV versions  ###
## Update Versions list below if new exist ##
#############################################
# Versions List #
rhel_ver = ["6","7","8","9"]
rhel_arm_ver = ["8","9"]
amz_ver = ["1","2","2023"]
amz_arm_ver = ["2","2023"]
sles_ver = ["11","12","15"]
#Debian versions have to be uploaded in a weird way to support repos, please follow the existing format to add a new repo
deb_ver = ["stretch","buster","bullseye","xenial","bionic","focal","jammy"]
deb_arm_ver = ["bionic","focal","jammy"] 


# Function to grab secrets
def get_secret(secid):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name="us-east-1")
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secid)
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secrets = json.loads(get_secret_value_response['SecretString'])
    if secid == "Sensor_Download_Key":
        sec1 = secrets['clientid']
        sec2 = secrets['clientsec']
    else:
        sec1 = secrets['afkey']
        sec2 = "dummykey"
    return sec1, sec2

def alert_slack(message):
    requests.post(slackhook, headers = {"Content-Type": "application/json"}, json = {"text": message})
    print("Slack Message Sent:",message)

def do_the_needful(filters,uri,env):
    response = falcon.command("GetCombinedSensorInstallersByQuery", filter=filters)
    try:
        name = response["body"]["resources"][0]["name"]
        sha = response["body"]["resources"][0]["sha256"]
        os = response["body"]["resources"][0]["os"]
        os_ver = response["body"]["resources"][0]["os_version"]

        if os == "Ubuntu":
            deb_dist = ""
            if "amd64" in name:
                arch = "x86_64"
                for i in deb_ver:
                    deb_dist = deb_dist + "deb.distribution=" + i + ";"
            elif "arm64" in name:
                arch = "arm64"
                for i in deb_arm_ver:
                    deb_dist = deb_dist + "deb.distribution=" + i + ";"
            else:
                message = ":warning: Hey,\nUnknown Arch found in Sensor Version Download Script\n" + name
                alert_slack(message)
            
            fname="falcon-sensor-current-" + env + '.' + arch +".deb"
            afurl=af_base + uri + fname + ";" + deb_dist + "deb.component=main;deb.architecture=" + arch
          
        elif os == "macOS" or os == "Windows":
            fname="current-" + env + '.' + name
            afurl=af_base + uri + fname

        elif os.startswith("RHEL") or os == "Amazon Linux" or os == "SLES":
            if "x86_64" in name:
                arch = ".x86_64"
            elif "aarch64" in name:
                os_ver = os_ver[0]
                arch = ".aarch64"
            else:
                message = ":warning: Hey,\nUnknown Arch found in Sensor Version Download Script\n" + name
                alert_slack(message)

            #Setnaming convention for Amzn vs RHEL
            if os.startswith("RHEL"):
                conv = "el"
            elif os == "Amazon Linux":
                conv = "amzn"
            elif os == "SLES":
                conv = "SLES"

            fname="falcon-sensor-current-" + env + '.' + conv + os_ver + arch +".rpm"
            afurl=af_base + uri + os_ver + "/" + fname

        else:
            pass
        
        path="/tmp/" + fname
        try:        
            #Download the installer
            download_response = falcond.download_sensor_installer(id=sha,
            download_path="/tmp/", file_name=fname)
        except:
            print("Error Downloading\n",os,env,fname)
        try:
            #Upload to Artifactory    
            response1=requests.put(afurl,auth=(afusername, afkey), data=open(path,'rb').read())
        except:
            print("Error Uploading ",os,env,fname)
        print("Installer Downloaded:\n",os,env,filters,"\n",name,download_response['body'])
        print(fname," Artifactory upload:",response1)

    except:
        print("Error with ",filters)

def macos(env, conn):
    #MacOS
    uri = "generic-edr-release/macos/" 
    filters="platform:'mac'+version:'"+vers["mac_"+env.lower()]+"'"
    do_the_needful(filters,uri,env)
    conn.send("macos done")
    conn.close()

def windows(env, conn):
    #Windows
    uri = "generic-edr-release/windows/" 
    filters="platform:'windows'+version:'"+vers["windows_"+env.lower()]+"'"
    do_the_needful(filters,uri,env)
    conn.send("windows done")
    conn.close()

    #Linux
def rhel(env, conn):
    #RHEL
    uri = "rpm-edr-release/el" 
    for i in rhel_ver:
        filters="platform:'linux'+os:'RHEL*'+os_version:'" + i + "'+version:'"+vers["linux_"+env.lower()]+"'"
        do_the_needful(filters,uri,env)
    conn.send("rhel done")
    conn.close()

def rhel_arm(env, conn):
    #RHEL ARM
    uri = "rpm-edr-release/el"
    for i in rhel_arm_ver:
        filters="platform:'linux'+os:'RHEL*'+os_version:'" + i + " - arm64'+version:'"+vers["linux_"+env.lower()]+"'"
        do_the_needful(filters,uri,env)
    conn.send("rhel_arm done")
    conn.close()


def amz(env, conn):
    #AMZ
    uri = "rpm-edr-release/amzn"
    for i in amz_ver:
        filters="platform:'linux'+os:'Amazon Linux'+os_version:'" + i + "'+version:'"+vers["linux_"+env.lower()]+"'"
        do_the_needful(filters,uri,env)
    conn.send("amz done")
    conn.close()

def amz_arm(env, conn):
    #AMZ ARM
    uri = "rpm-edr-release/amzn"
    for i in amz_arm_ver:
        filters="platform:'linux'+os:'Amazon Linux'+os_version:'" + i + " - arm64'+version:'"+vers["linux_"+env.lower()]+"'"
        do_the_needful(filters,uri,env)
    conn.send("amz_arm done")
    conn.close()

    #SLES
def sles(env, conn):
    uri = "rpm-edr-release/SLES"
    for i in sles_ver:
        filters="platform:'linux'+os:'SLES'+os_version:'" + i + "'+version:'"+vers["linux_"+env.lower()]+"'"
        do_the_needful(filters,uri,env)
    conn.send("sles done")
    conn.close()

def deb(env, conn):
    #Deb x86_64 
    uri = "debian-edr-release/"
    filters="platform:'linux'+os:'Ubuntu'+os_version:!'*arm64'+version:'"+vers["linux_"+env.lower()]+"'"
    do_the_needful(filters,uri,env)
    conn.send("deb done")
    conn.close()

def deb_arm(env, conn):
    #Deb arm64
    uri = "debian-edr-release/"
    filters="platform:'linux'+os:'Ubuntu'+os_version:'*arm64'+version:'"+vers["linux_"+env.lower()]+"'"
    do_the_needful(filters,uri,env)
    conn.send("deb_arm done")
    conn.close()

def lambda_handler(event, context):
    print("Congrats! It's time to run this puppy and update the Sensor Installers!!!")
    global afkey, falcon, falcond, vers
    vers = {}
    print("Logging In")
    clientid, clientsec = get_secret("Sensor_Download_Key")
    afkey, afdummykey = get_secret("Artifactory_User_Key")
    falcon = APIHarness(client_id=clientid, client_secret=clientsec)
    falcond = SensorDownload(client_id=clientid, client_secret=clientsec)
    
    #Get Current Dev/Prd Version Numbers
    for name,pol in pols.items():
        version = falcon.command("getSensorUpdatePoliciesV2", ids=pol)["body"]["resources"][0]["settings"]["sensor_version"]
        add = {name: version}
        vers.update(add)
    time.sleep(15)
    #Setup the multiprocess thread
    processes = []
    parent_connections = []
    instances = [macos, windows, rhel, rhel_arm, amz, amz_arm, sles, deb, deb_arm]


    start = time.time()
    for env in environ:
        for instance in instances:
            #create a pipe for communication
            parent_conn, child_conn = Pipe()
            parent_connections.append(parent_conn)

            #create the process, pass instance and pipe as arguments
            process = Process(target=instance, args=(env, child_conn))
            processes.append(process)

    #start the processes
    for process in processes:
        process.start()

    #make sure all processes have finished
    for process in processes:
        process.join()
    
    print("All processes are done, Time to complete transfer: ", time.time() - start)
    time.sleep(120)

    message = "The Sensor Installer Updater script has completed. :lambda_lambda_lambda:"
    alert_slack(message)
    print("\n**********************")
    print("**Transfers Complete!*")
    print("**********************")
