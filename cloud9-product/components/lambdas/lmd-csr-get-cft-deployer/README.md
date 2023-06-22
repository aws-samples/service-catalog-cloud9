# Get CloudFormation Deployer

[Tracking AWS Service Catalog products provisioned by individual SAML users](https://aws.amazon.com/blogs/mt/tracking-aws-service-catalog-products-provisioned-by-individual-saml-users/)

When deploying AWS Cloud9, by default, the Cloud 9 environment is assigned to the user who launches it.

However, when Cloud 9 is launched from Service Catalog, it is assigned to a Service Catalog [service role](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/service-role.html).  

Our solution is to store the user who launched the Service Catalog product by creating an [AWS Event Bridge](https://aws.amazon.com/eventbridge/) that is sent from [AWS CloudTrail](https://aws.amazon.com/cloudtrail/).  

Once the user name is stored in an [Amazon DynamoDB](https://aws.amazon.com/dynamodb/), the ```lmd-csr-get-cft-deployer``` Lambda implements a CloudFormation custom resource that retrieves the original user who launched the CloudFormation stack.

## Usage

See the inline comments for usage.

```yaml
Resources:
  # The process of capturing the user via an EventBridge event is asynchronous.
  # Give the process time to complete
  WaitForCloudTrail:
    Type: 'AWS::CloudFormation::CustomResource'
    Properties:
      ServiceToken: !ImportValue CFNSleep
      SleepSeconds: "20"

  # Call the Lambda to retrieve the logged in UserId based on the StackId
  CFUser:
      Type: 'Custom::CFGetUser'
      Version: "1"
      # Wait 20 seconds before trying to create the resource
      DependsOn: WaitForCloudTrail
      Properties:
        ServiceToken: !ImportValue CFNGetStackCreator
        # The user is stored for each created Stack
        StackId: !Ref AWS::StackId
  C9IDE:
    Type: 'AWS::Cloud9::EnvironmentEC2'
    Properties:
      # Name the Cloud9 environment based on the user who created it.
      Name: !Sub  '${CFUser.Id}-${Env}-Cloud9-IDE'
      ....
      # Reassign the user id from the service role to the correct user.
      OwnerArn: !GetAtt CFUser.Arn
      ConnectionType: "CONNECT_SSM"

```
