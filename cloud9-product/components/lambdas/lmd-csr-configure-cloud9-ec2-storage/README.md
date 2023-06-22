# AWS CloudFormation Custom Resource to Configure storage space for Cloud 9 

[AWS Cloud9](https://aws.amazon.com/cloud9/) is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser. It includes a code editor, debugger, and terminal.

When you create a Cloud9 environment, an [EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instances-and-amis.html) is provisioned for you with 10GB of [EBS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volumes.html) storage containing development tools.  

AWS CloudFormation provides a [method](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html) to automate provisioning of Cloud 9 environments.  But it does not allow you to specify the amount of storage for your environment.

The ```lmd-csr-configure-cloud9-ec2-storage``` Lambda function implements a CloudFormation custom resource that allows you to configure the amount of storage for your EC2 based Cloud9 environment.

[AWS CloudFormation custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) enable you to write custom provisioning logic in templates that AWS CloudFormation runs anytime you create, update (if you changed the custom resource), or a delete stack.


## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

```yaml
Resources:
  ConfigureCloud9Storage:
    Type: 'Custom::CFNResizeCloud9Volume'
    Properties: 
      ServiceToken:
        Fn::ImportValue: CFNResizeCloud9Volume
      EnvironmentId: <Cloud9InstanceId>
      VolumeSize: <integer>
```

## Properties

### ServiceToken

Always ```!ImportValue CFNResizeCloud9Volume```

### EnvironmentId

The Cloud9 instance id.

### VolumeSize

The desired amount of storage.  The  Lambda will modify the size of the underlying EBS volume and restart the EC2 instance.

## Return values

### Ref

None

### Fn::GetAtt

The Fn::GetAtt intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the Fn::GetAtt intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

### VolumeSize

The new size of the underlying volume

## Example

```yaml
Resources:
  Cloud9VolumeResize:
    Type: 'Custom::CFNResizeCloud9Volume'
    Properties: 
      ServiceToken:
        Fn::ImportValue: CFNResizeCloud9Volume
      EnvironmentId: !Ref Cloud9Instance
      VolumeSize: 50
  Cloud9Instance:
    Type: 'AWS::Cloud9::EnvironmentEC2'
    Properties:
      AutomaticStopTimeMinutes: 30
      ConnectionType: CONNECT_SSM
      InstanceType: m3.medium
      Name: MyCloud9Environment
      ImageId: "amazonlinux-2-x86_64"

```