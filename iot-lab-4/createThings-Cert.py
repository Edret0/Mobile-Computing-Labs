################################################### Connecting to AWS
import boto3
import json
################################################### Create random name for things
import random
import string

################################################### Parameters for Thing
defaultPolicyName = 'policy_car' # My policy name
thingGroupName = 'car_group'  # Thing group name to attach the 500 things
###################################################

def createThing(): # Method to create a thing
    thingName = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
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
            addThingToThingGroup(thingName)  # Add the thing to the thing group 

def createCertificate(thingName):  # Method to create a certificate for a thing
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

def addThingToThingGroup(thingName): # Method to add a thing to the thing group
    response = thingClient.add_thing_to_thing_group(
        thingGroupName=thingGroupName,
        thingName=thingName
    )

thingClient = boto3.client('iot')
for i in range(500): # Loop to create 500 things
    createThing()