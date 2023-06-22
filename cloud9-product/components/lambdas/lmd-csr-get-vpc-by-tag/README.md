# Get VPC by Tag CloudFormation Custom Resource

[CloudFormation custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) enable you to write custom provisioning logic in templates that AWS CloudFormation runs anytime you create, update (if you changed the custom resource), or a delete stack.

The ```lmd-csr-get-vpc-by-tag``` Lambda function implements a custom resource that retrieves a VPC by tag. This allows network administrators to specify VPCs to be used by DevOps engineers when deploying a CloudFormation stack.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

```yaml
Type: Custom::GetVpcsByTag
Properties:
  ServiceToken: !ImportValue CFNGetVpcsByTag
  VpcId: VpcId
  Tags:
    - Key: keyName
      Value: keyValue
  Nonce: !Ref Nonce
```

## Properties

### ServiceToken

Always ```!ImportValue CFNGetSecurityGroupsByTag```

### Nonce

CloudFormation will not run a custom resource on update if none of the properties of the resource change.  This forces CloudFormation to search your AWS account on an update by passing in a random string.

### Tags

A list of tag keys and values

## Return values

### Ref

Returns a hash of the response.  It is for internal use only

### Fn::GetAtt

The Fn::GetAtt intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the Fn::GetAtt intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

### SecurityGroups

A list of security groups containing matching the tag names and values.


## Example

This is an example of a CloudFormation template that retrieves a VPCId, subnets and security group ids based on tags.

```yaml

Resources:
  LambdaVpc:
      Type: 'Custom::GetVpcByTag'
      Properties:
        ServiceToken: !ImportValue CFNGetVpcsByTag
        Tags:
          - Key: application
            Value: app1
          - Key: department
            Value: finance

  LambdaSecurityGroup:
      Type: 'Custom::GetSecurityGroupByTag'
      Properties:
        VpcId: !Ref LambdaVpc
        Tags:
          - Key: application
            Value: app1
          - Key: department
            Value: finance

  LambdaSubnet:
      Type: 'Custom::GetSubnetsByTags'
      Properties:
        VpcId: !Ref LambdaVpc
        Tags:
          - Key: application
            Value: app1
          - Key: department
            Value: finance

  Lambda:
    Type: AWS::Lambda::Function
    Properties :
        Code :
            S3Bucket: example
            S3Key: mylambda
        Runtime : Python3.7
        Role: LambdaRole
        VpcConfig :
            SecurityGroupIds: !GetAtt LambdaSecurityGroup.SecurityGroups
            SubnetIds: !GetAtt LambdaSubnet.Subnets

  LambdaRole:
    Type: "AWS::IAM::Role"
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          -
            Effect: "Allow"
            Principal:
              Service:
                - lambda.amazonaws.com
                - events.amazonaws.com
            Action:
              - "sts:AssumeRole"
```