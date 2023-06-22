import json
import boto3
import cfnresponse as cfnresponse
import re


c9_client = boto3.client('cloud9')
cft_client = boto3.client("cloudformation")

def lambda_handler(event, context):
    print(json.dumps(event))
    try:
        if event["RequestType"] == "Delete":
            cfnresponse.send(event, context, cfnresponse.SUCCESS,responseData={})
            return
        props = event['ResourceProperties']        
        required_props=["StackId"]
        cfnresponse.validate_resource_properties(event["ResourceProperties"],required_props)

        # Get the name of the Cloud9 instance
        cloud9_id = props["EnvironmentId"]
        response = c9_client.describe_environments(environmentIds=[cloud9_id])
        name = response["environments"][0]["name"]
        name = re.sub(r'[^a-zA-Z0-9\s]', '-', name)
        #Cloud9 CloudFormation stacks are created in a known format.  
        cloud9_stackname = f"aws-cloud9-{name}-{cloud9_id}"

        # Cloud9 Creates a stack with two resources -- an EC2 instance and a Security Group.
        response = cft_client.describe_stack_resource(StackName=cloud9_stackname,LogicalResourceId='InstanceSecurityGroup')
        security_group = response["StackResourceDetail"]["PhysicalResourceId"]
        response = cft_client.describe_stack_resource(StackName=cloud9_stackname,LogicalResourceId='Instance')
        instance_id = response["StackResourceDetail"]["PhysicalResourceId"]

        cfnresponse.send(event, context, cfnresponse.SUCCESS, {
          "InstanceId":instance_id,
          "SecurityGroupId":security_group},physicalResourceId=instance_id)
    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {},reason=str(e))

