import cfnresponse
import boto3
from botocore.exceptions import ClientError
import json
import re
import time

def get_cloud9_stack_name(cloud9_id):
    c9_client = boto3.client('cloud9')
    response = c9_client.describe_environments(environmentIds=[cloud9_id])
    name = response["environments"][0]["name"]
    name = re.sub(r'[^a-zA-Z0-9\s]', '-', name)
    stack_name = f"aws-cloud9-{name}-{cloud9_id}"
    return stack_name

def modify_volume_size(stack_name, volume_size):
    # Create EC2 client
    ec2 = boto3.client('ec2')

    # Get the instance id of the EC2 instance used for the environment
    response = boto3.client('cloudformation').describe_stack_resource(StackName=stack_name, LogicalResourceId='Instance')
    instance_id = response['StackResourceDetail']['PhysicalResourceId']

    # Get the attached volume of the EC2 instance that backs your build environment
    response = ec2.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}])
    print(response)
    volume_id = response['Volumes'][0]['VolumeId']

    # Wait until the volume is not in the "optimizing" state
    volume_status = ""
    try:
        response = ec2.describe_volumes_modifications(VolumeIds=[volume_id])
        if response['VolumesModifications']:
            volume_status = response['VolumesModifications'][0]['ModificationState']
    except ClientError as e:
        if e.response['Error']['Code'] == "InvalidVolumeModification.NotFound":
            volume_status = ""
    

    print("volume_status",volume_status)
    start_time = time.time()
    while volume_status == "optimizing":
        print("volume_status",volume_status)
        print("Waiting...")
        if time.time() - start_time > 300:
            raise Exception(f"Timed out waiting for volume {volume_id} to be out of the optimizing state")
        time.sleep(5)
        response = ec2.describe_volumes_modifications(VolumeIds=[volume_id])
        if not response['VolumesModifications'] or response['VolumesModifications'][0]['ModificationState'] not in ["modifying","optimizing"]:
            # Volume is not being modified, so it's safe to proceed
            break
        volume_status = response['VolumesModifications'][0]['ModificationState']
        print("Volume Status = "+ volume_status)

    # Change the size of the volume to the specified size
    ec2.modify_volume(VolumeId=volume_id, Size=volume_size)

    # Reboot the instance
    ec2.reboot_instances(InstanceIds=[instance_id])

    # Wait for the instance to reboot
    waiter = ec2.get_waiter('instance_status_ok')
    waiter.wait(InstanceIds=[instance_id])

    print(f"Successfully modified volume size to {volume_size} GB")




def lambda_handler(event, context):
    props = event['ResourceProperties']
    print(json.dumps(event))
    try:
        if event["RequestType"] == "Delete":
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
            return

        # Check if the required properties are present
        required_props = ["EnvironmentId", "VolumeSize"]
        cfnresponse.validate_resource_properties(props, required_props)

        # Get the Cloud9 stack name using the provided environment ID
        cloud9_id = props["EnvironmentId"]
        stack_name = get_cloud9_stack_name(cloud9_id)

        # Modify the volume size using the derived stack name and provided volume size
        modify_volume_size(stack_name, int(props["VolumeSize"]))

        # Send a success response back to CloudFormation with the updated volume size
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {"VolumeSize": props["VolumeSize"]})

    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, reason=str(e))
