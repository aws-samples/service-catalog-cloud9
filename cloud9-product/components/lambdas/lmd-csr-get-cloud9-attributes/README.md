# AWS CloudFormation Custom Resource to Configure storage space for Cloud 9 

[AWS Cloud9](https://aws.amazon.com/cloud9/) is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser. It includes a code editor, debugger, and terminal.

When you create a Cloud9 environment, an [EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instances-and-amis.html) and a [security group](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html) are provisioned.


These two resources are not exposed by the ```[!GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html)``` CloudFormation intrinsic function.

For instance you may need to know the security group provisioned so that your users can connect to other resources in your account such as databases via a [security group ingress rule](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html)


The ```lmd-csr-get-cloud9-attributes``` Lambda function implements a CloudFormation custom resource that allows you to retrieve the security group Id and the EC2 instance Id of the security group and EC2 instance created by Cloud 9.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

```yaml
Resources:
# Call the Lambda custom resource
  GetCloud9Attributes:
      Type: 'Custom::CFNGetCloud9Properties'
      Properties:
        ServiceToken: !ImportValue CFNGetCloud9Properties
        EnvironmentId: !Ref 'C9IDE'
```

## Properties

### ServiceToken

Always ```!ImportValue CFNGetCloud9Properties```

### EnvironmentId

The Cloud9 instance id.

## Return values

### Ref

None

### Fn::GetAtt

The Fn::GetAtt intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the Fn::GetAtt intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

### InstanceId

The Id of the EC2 instance launched by Cloud9

### SecurityGroupId

The Id of the SecurityGroup created by Cloud9

## Example

```yaml
Resources:
# Call the Lambda custom resource
  CFNGetCloud9:
      Type: 'Custom::CFNGetCloud9Properties'
      Properties:
        ServiceToken: !ImportValue CFNGetCloud9Properties
]        EnvironmentId: !Ref 'C9IDE'
# Create the Cloud9 Environment
  C9IDE:
    Type: 'AWS::Cloud9::EnvironmentEC2'
    Properties:
        ...

  SecurityGroupIngres:
     Type: 'AWS::EC2::SecurityGroupIngress'
     Properties:
       # Use the security group of the Cloud9 environment
       SourceSecurityGroupId: !GetAtt CFNGetCloud9.SecurityGroupId 
       GroupId: <your security group>
       IpProtocol: all
       ToPort: "5432"


```