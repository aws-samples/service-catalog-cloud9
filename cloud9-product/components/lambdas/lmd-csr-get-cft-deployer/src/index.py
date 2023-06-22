import json
import time
import cfnresponse as cfnresponse
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    if event["RequestType"] == "Delete":
        cfnresponse.send(event, context, cfnresponse.SUCCESS,responseData={})
        return             
    print(json.dumps(event))
    try:
        required_props=["StackId"]
        cfnresponse.validate_resource_properties(event["ResourceProperties"],required_props)
        stackId = event['ResourceProperties']['StackId']
        Id = (stackId.split('/'))[-1]

        userAid=get_user_aid(Id)
        cfnresponse.send(event, context, cfnresponse.SUCCESS,userAid,physicalResourceId=userAid["Arn"])  # type: ignore
    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {},reason=str(e))

def get_user_aid(stackId):

    IValue = ''
    table = dynamodb.Table('sc-track-user')
    counter = 0

    while not IValue:
        try:
            response = table.get_item(
                Key={
                    'CFStackid': stackId
                }
            )
            if 'Item' in response:
                IValue = {
                    "Id":response['Item']['User'],
                    "Arn":response["Item"]["Arn"]
                    }
            else:
                time.sleep(5)

        except ClientError as e:
            print(e.response['Error']['Message'])
            raise e
        return(IValue)


