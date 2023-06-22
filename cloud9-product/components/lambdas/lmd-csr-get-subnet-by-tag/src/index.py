import cfnresponse as cfnresponse
import boto3
import json
import re

client = boto3.client('ec2')

def get_subnets(vpc_id, tags, one_subnet_per_az=False):
    filters = [{"Name": "vpc-id", "Values": [vpc_id]}]
    for tag in tags:
            filters.append({"Name": f"tag:{tag['Key']}", "Values": [tag['Value']]})
    response = client.describe_subnets(Filters=filters)
    subnets = []
    availability_zones = []
    seen_azs = set()
    for subnet in response["Subnets"]:
        if one_subnet_per_az and subnet["AvailabilityZone"] in seen_azs:
            continue
        subnets.append(subnet["SubnetId"])
        availability_zone = subnet["AvailabilityZone"]
        availability_zones.append(availability_zone)
        seen_azs.add(availability_zone)
    return {
        "Subnets": subnets,
        "AvailabilityZones": availability_zones
    }


def lambda_handler(event, context):
    props = event['ResourceProperties']
    try:
        if event["RequestType"] == "Delete":
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
            return
        required_props = ["Tags", "VpcId"]
        cfnresponse.validate_resource_properties(event["ResourceProperties"], required_props)
        one_subnet_per_az = props.get("OneSubnetPerAZ", False)
        response = get_subnets(props["VpcId"], props["Tags"], one_subnet_per_az)
        if len(response["Subnets"]) == 0:
            raise Exception(f"No subnets found matching tags {props['Tags']}")
        cfnresponse.send(event, context, cfnresponse.SUCCESS, response)
        print(response)
    except Exception as e:
        print(str(e))
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, reason=str(e))
