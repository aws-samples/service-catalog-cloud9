# Get Subnets by Tag CloudFormation Custom Resource

[CloudFormation custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) enable you to write custom provisioning logic in templates that AWS CloudFormation runs anytime you create, update (if you changed the custom resource), or a delete stack.

The ```lmd-csr-get-subnet-by-tag``` Lambda function implements a custom resource that retrieves a list of subnets  based on a list of tag keys and values. This allows network administrators to specify subnets to be used by DevOps engineers when deploying a CloudFormation stack.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

```yaml
Type: Custom::GetSubnetsByTag
Properties:
  ServiceToken: !ImportValue CFNGetSubnetsByTag
  VpcId: VpcId
  OneSubnetPerAZ: <boolean> (optional)
  Tags:
    - Key: <keyname>
      Value: <string or regular expressio>
  Nonce: <A random string>
```

## Properties
### Nonce

CloudFormation will not run a custom resource on update if none of the properties of the resource change.  This forces CloudFormation to search your AWS account on an update by passing in a random string.

### ServiceToken

Always ```!ImportValue CFNGetSubnetsByTag```

### Tags

A list of tag keys and values

### VpcId

The ID of the VPC containing the subnet.

### OneSubnetPerAZ

With autoscaling groups, you can only specify one subnet per AZ.  If this property is set to ```True```, only one subnet will be returned for each available zone regardless of the number of matching subnets.

### Nonce

CloudFormation will not run a custom resource on update if none of the properties of the resource change.  This forces CloudFormation to search your AWS account on an update by passing in a random string.

## Return values

### Ref

Returns a hash of the response.  It is for internal use only

### Fn::GetAtt

The Fn::GetAtt intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the Fn::GetAtt intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

### Subnets

A list of Subnets containing matching names and values.

### AvailabilityZones

A list of the availability zones where the subnets are contained.  This is useful when retrieving subnets to use for Autoscaling groups.

## Example

This is an example of a CloudFormation template that retrieves a VPCId, subnets and security group ids based on tags.

```yaml
Resources:
  Vpc:
      Type: 'Custom::GetVpcByTag'
      Properties:
        ServiceToken: !ImportValue CFNGetVpcsByTag
      Tags:
        - Key: application
          Value: app1
        - Key: department
          Value: finance
  
  ## Call the custom resource to retrieve the subnets based on the tag keys
  Ec2Subnets:
    Type: 'Custom::GetSubnetsByTag'
    Version: 1
    Properties:
      ServiceToken: !ImportValue CFNGetSubnetsByTag
      VpcId: !Select 
        - 0
        - !GetAtt  Vpc.VpcIds
      Tags:
        - Key: application
          Value: app1
        - Key: department
          Value: finance
        ## Values can also contain astericks
        - Key: Name
          Value: "*-public"
  SecurityGroups:
    Type: 'Custom::GetSecurityGroupsByTag'
    Condition: UseVpc
    Version: 1
    Properties:
      ServiceToken: !ImportValue CFNGetSecurityGroupsByTag
      VpcId: !Select 
        - 0
        - !GetAtt  Vpc.VpcIds
      Tags:
        - Key: application
          Value: app1
        - Key: department
          Value: finance
  WebServerGroup:
   Type: 'AWS::AutoScaling::AutoScalingGroup'
   Properties:
     AvailabilityZones: !GetAtt Ec2Subnets.AvailabilityZones
     VPCZoneIdentifier: !GetAtt Ec2Subnets.Subnets
     DesiredCapacity: !Ref MinInstances
     HealthCheckGracePeriod: 300
     TargetGroupARNs:
      - !Ref AlbTargetGroup
     HealthCheckType: EC2
     LaunchTemplate:
       LaunchTemplateId: !Ref LaunchTemplate
       Version: !GetAtt LaunchTemplate.LatestVersionNumber
     MaxSize: !Ref MaxInstances
     MinSize: !Ref MinInstances
```


