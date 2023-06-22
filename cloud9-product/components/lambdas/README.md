# CloudFormation data sources

This repository contains AWS CloudFormation custom resources which allow you to reference existing infrastructure in your AWS Virtual Private Cloud (VPC) based on a list of tags within your template.

This allows network administrators to specify security resources to be used by DevOps engineers when deploying a CloudFormation stack.

[CloudFormation custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) enable you to write custom provisioning logic in templates that AWS CloudFormation runs anytime you create, update (if you changed the custom resource), or a delete stack.

## Custom resources contained in this repository

[Get Security Group by Tag](./components/lambdas/lmd-csr-get-securitys-group-by-tag/)

Implements a custom resource that retrieves a list of security groups  based on a list of tag keys and values.

[Get Subnets by Tag](./components/lambdas/lmd-csr-get-subnet-by-tag/)


Implements a custom resource that retrieves a list of subnets  based on a list of tag keys and values.

[Get VPC by Tag](./components/lambdas/lmd-csr-get-vpc-by-tag/)

Implements a custom resource that retrieves a VPC by a list of  tag keys and values.


## Deployment

### Using AWS CloudShell

The most straightforward method to deploy this solution involves logging into your AWS account with the appropriate permissions and using [AWS CloudShell](https://aws.amazon.com/cloudshell/)

Log into your AWS account, navigate to the Cloudshell page and clone the repository.

```bash
cd components/lambdas
# Run static code analysis tools -- cfn-validate,cfn-nag and Bandit
bash scan.sh
# Deploy the Lambdas
bash deploy.sh
```

### Deploying locally

#### Prerequisites

- [AWS SAM prerequisites](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/prerequisites.html) 
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) When deploying locally instead of using CloudShell, the deployment script uses Docker to build the Lambdas with the proper dependencies.

From the terminal, after you clone the repository, run the following commands.

```bash
cd components/lambdas
# Run static code analysis tools -- cfn-validate,cfn-nag and Bandit
bash scan.sh
# Deploy the Lambdas
bash deploy.sh
```