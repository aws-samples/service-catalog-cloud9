# Store CloudFormation Deployer

[Tracking AWS Service Catalog products provisioned by individual SAML users](https://aws.amazon.com/blogs/mt/tracking-aws-service-catalog-products-provisioned-by-individual-saml-users/)

When deploying AWS Cloud9, by default, the Cloud 9 environment is assigned to the user who launches it.

However, when Cloud 9 is launched from Service Catalog, it is assigned to a Service Catalog [service role](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/service-role.html).  

Our solution is to store the user who launched the Service Catalog product by creating an [AWS Event Bridge](https://aws.amazon.com/eventbridge/) that is sent from [AWS CloudTrail](https://aws.amazon.com/cloudtrail/).  It then triggers the ```lmd-csr-store-cft-deployer``` Lambda.
