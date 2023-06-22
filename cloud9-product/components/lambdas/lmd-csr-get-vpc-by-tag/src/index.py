import cfnresponse as cfnresponse
import boto3
import json

client = boto3.client('ec2')

def get_vpc(tags):
    filters = []
    for tag in tags:
        filters.append({
            "Name": f"tag:{tag['Key']}",
            "Values": [tag['Value']]
        })
    response = client.describe_vpcs(Filters=filters)
    result = list(map(lambda s: s["VpcId"], response["Vpcs"]))
    print(json.dumps(result, indent=2))
    return result

def lambda_handler(event, context):
    props = event['ResourceProperties']
    print(json.dumps(event))
    try:
        if event["RequestType"] == "Delete":
            cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData={})
            return
        required_props = ["Tags"]
        cfnresponse.validate_resource_properties(event["ResourceProperties"], required_props)
        response = get_vpc(props["Tags"])
        if len(response) == 0:
            raise Exception(f"No VPCs with the specified tags")
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {"VpcIds": response})
    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, reason=str(e))
