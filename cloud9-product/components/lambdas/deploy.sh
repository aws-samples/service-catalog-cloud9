# Build and deploy lambdas. This will automatically build 
# any Lambda based on a template in the ./custom-resources/template

set -e

if ls ./*.yml 1> /dev/null 2>&1; then
   exit 0
fi




for dir in  */; do \
        echo "Processing directory: $dir";
        templates="$dir""*.yml"
        for template in $templates; do
                echo "Processing template: $template";
                stackname=$(basename ${template} ".yml");
                if [ -n "${CODEBUILD_BUILD_ID+x}" ] || [[ "${AWS_EXECUTION_ENV}" == *"CloudShell"* ]]; then
                        sam build -t $template
                else
                        sam build -t $template --use-container;
                fi
                sam deploy  --template-file  .aws-sam/build/template.yaml  --stack-name $stackname \
                        --capabilities CAPABILITY_NAMED_IAM CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
                        --resolve-s3 \
                        --no-fail-on-empty-changeset \
                        --parameter-overrides Nonce=$RANDOM
        done
done

