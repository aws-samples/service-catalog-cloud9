


set -e

# https://docs.aws.amazon.com/cloud9/latest/user-guide/ec2-ssm.html
# These commands must be run to create an SSM Connection 

export AWS_PAGER=""

echo "1"
if ! aws iam get-role --role-name AWSCloud9SSMAccessRole >/dev/null 2>&1; then
    aws iam create-role --role-name AWSCloud9SSMAccessRole --path /service-role/ --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Principal": {"Service": ["ec2.amazonaws.com","cloud9.amazonaws.com"]      },"Action": "sts:AssumeRole"}]}'
else
    echo "IAM role AWSCloud9SSMAccessRole already exists."
fi

echo "2"
if [ -z "$(aws iam list-attached-role-policies --role-name AWSCloud9SSMAccessRole --query 'AttachedPolicies[?PolicyArn==`arn:aws:iam::aws:policy/AWSCloud9SSMInstanceProfile`].PolicyArn' --output text)" ]; then
    aws iam attach-role-policy --role-name AWSCloud9SSMAccessRole --policy-arn arn:aws:iam::aws:policy/AWSCloud9SSMInstanceProfile
else
    echo "AWSCloud9SSMInstanceProfile policy already attached to AWSCloud9SSMAccessRole."
fi

echo "3"
if ! aws iam get-instance-profile --instance-profile-name AWSCloud9SSMInstanceProfile >/dev/null 2>&1; then
    aws iam create-instance-profile --instance-profile-name AWSCloud9SSMInstanceProfile --path /cloud9/
else
    echo "IAM instance profile AWSCloud9SSMInstanceProfile already exists."
fi

echo "4"
if ! aws iam list-instance-profiles-for-role --role-name AWSCloud9SSMAccessRole --query 'InstanceProfiles[?InstanceProfileName==`AWSCloud9SSMInstanceProfile`].InstanceProfileName' --output text >/dev/null 2>&1; then
    aws iam add-role-to-instance-profile --instance-profile-name AWSCloud9SSMInstanceProfile --role-name AWSCloud9SSMAccessRole
else
    echo "IAM role AWSCloud9SSMAccessRole already added to instance profile AWSCloud9SSMInstanceProfile."
fi



echo "Deploying Lambdas"
pushd components/lambdas
bash deploy.sh
popd