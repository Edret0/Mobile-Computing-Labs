# Connecting to AWS: Imports boto3 library for interacting with AWS services and json for handling JSON data
import boto3
import json

# Importing this module to be used to create random name for things
import random
import string

# Parameters for Thing
defaultPolicyName = 'policy_car' # My policy name
thingGroupName = 'car_group'  # Thing group name to attach the 500 things

###################################################

# createThing() Function: Creates a thing in AWS IoT Core. 
# It generates a random name for the thing, creates a certificate for the thing, and adds the thing to a specified thing group.
def createThing(): 
    thingName = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)]) # Generates random names for the IoT things to be created using a combination of lowercase and uppercase letters along with digits
    global thingClient
    thingResponse = thingClient.create_thing(
        thingName=thingName
    )
    data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
    for element in data:
        if element == 'thingArn':
            thingArn = data['thingArn']
        elif element == 'thingId':
            thingId = data['thingId']
            createCertificate(thingName) # Create a certificate for this thing
            addThingToThingGroup(thingName)  # Add the thing to a thing group 

######################################################

# createCertificate() Function: Creates a certificate for a thing. 
# It also generates public and private keys for the certificate, writes them to files, and attaches the certificate to a policy and the thing.
def createCertificate(thingName): 
    global thingClient
    certResponse = thingClient.create_keys_and_certificate(
        setAsActive=True
    )
    data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
    for element in data:
        if element == 'certificateArn':
            certificateArn = data['certificateArn']
        elif element == 'keyPair':
            PublicKey = data['keyPair']['PublicKey']
            PrivateKey = data['keyPair']['PrivateKey']
        elif element == 'certificatePem':
            certificatePem = data['certificatePem']
        elif element == 'certificateId':
            certificateId = data['certificateId']

    with open(f'public_{thingName}.key', 'w') as outfile: # Public key for the thing
        outfile.write(PublicKey)
    with open(f'private_{thingName}.key', 'w') as outfile: # Private key for the thing
        outfile.write(PrivateKey)
    with open(f'cert_{thingName}.pem', 'w') as outfile: # Certificate for the thing
        outfile.write(certificatePem)

    response = thingClient.attach_policy(
        policyName=defaultPolicyName,
        target=certificateArn
    )
    response = thingClient.attach_thing_principal(
        thingName=thingName,
        principal=certificateArn
    )

#########################################################
    
# addThingToThingGroup() Function: Add a thing to a thing group
def addThingToThingGroup(thingName): 
    response = thingClient.add_thing_to_thing_group(
        thingGroupName=thingGroupName,
        thingName=thingName
    )

##########################################################
    
#Initializing an AWS IoT client using the Boto3 library    
thingClient = boto3.client('iot')

##########################################################

# Main Loop to create 500 things
for i in range(500): 
    createThing()