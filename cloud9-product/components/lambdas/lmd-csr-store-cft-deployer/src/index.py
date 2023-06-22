import boto3
import json

def lambda_handler(event, context):
    print(json.dumps(event))
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('sc-track-user')
    if event['detail']['responseElements'] is  None:
        return
    stackId = event['detail']['responseElements']['stackId']
    Id = (stackId.split('/'))[-1]
    UserArn = event['detail']['userIdentity']['arn']
    UserAID = (UserArn.split('/'))[-1]
    table.put_item(
        Item={
            'CFStackid' : Id,
            'User' : UserAID,
            "Arn":UserArn
        })