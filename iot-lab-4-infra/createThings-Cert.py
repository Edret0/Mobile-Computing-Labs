import boto3
import json
import os
import random
import string

defaultPolicyName = 'policy_car'
thingGroupName = 'car_group'

def createThing(index): 
    thingName = f'thing_{index}'
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
            createCertificate(thingName, index)
            addThingToThingGroup(thingName)

def createCertificate(thingName, index): 
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

    os.makedirs(f'certificates/{index}', exist_ok=True)
    os.makedirs(f'public_certificates/{index}', exist_ok=True)
    os.makedirs(f'private_certificates/{index}', exist_ok=True)

    with open(f'certificates/{index}/cert_{thingName}.pem', 'w') as outfile: 
        outfile.write(certificatePem)
    with open(f'public_certificates/{index}/public_{thingName}.key', 'w') as outfile: 
        outfile.write(PublicKey)
    with open(f'private_certificates/{index}/private_{thingName}.key', 'w') as outfile: 
        outfile.write(PrivateKey)

    response = thingClient.attach_policy(
        policyName=defaultPolicyName,
        target=certificateArn
    )
    response = thingClient.attach_thing_principal(
        thingName=thingName,
        principal=certificateArn
    )

def addThingToThingGroup(thingName): 
    response = thingClient.add_thing_to_thing_group(
        thingGroupName=thingGroupName,
        thingName=thingName
    )

thingClient = boto3.client('iot')

#for i in range(3, 100):
#createThing(i)