
set -e

export $(aws cloudformation describe-stacks  --stack-name $PortfolioStackName --output text --query 'Stacks[0].Outputs[].join(`=`, [join(`_`, [`CF`, `OUT`, OutputKey]), OutputValue ])')

export $(aws cloudformation describe-stacks  --stack-name $PortfolioStackName --output text --query 'Stacks[0].Outputs[].join(`=`, [join(`_`, [`CF`, `OUT`, OutputKey]), OutputValue ])')

export ScriptsDir=$BASEDIR/three-stage-cross-account-pipeline/scripts



export ServiceCatalogRoleName=$CF_OUT_ServiceCatalogCloudFormationRole

bash deploy-service-catalog-product.sh \
     $BASEDIR/cloud9-product/cloud9-product.yml \
     $BASEDIR/cloud9-product/cloud9-sc-parameters.json \
      cloud9-product 


