#!/bin/bash

account_number=$(cat ../config.json | jq .MASTER_ACCOUNT_NUMBER)
profile=$(cat ../config.json | jq .PROFILE)
region=$(cat ../config.json | jq .REGION)
role=$(cat ../config.json | jq .MASTER_ROLE_NAME)
rule_name=$(cat ../config.json | jq .CW_RULE_NAME)

reg=$(echo $"$region" | tr -d '"')
acc=$(echo $"$account_number" | tr -d '"')
r=$(echo $"$role" | tr -d '"')
prf=$(echo $"$profile" | tr -d '"')
rulen=$(echo $"$rule_name" | tr -d '"')

new_role=arn:aws:iam::$acc:role/$r
echo $reg
echo $new_role

sed -i -e "s/running_local = True/running_local = False/g" $(pwd)/utils/profile.py
sed -i -e "s/REGION/$reg/g" $(pwd)/lambda.json
sed -i -e "s@ROLE@$new_role@g" $(pwd)/lambda.json


if [ ! -f ~/.aws/credentials ]; then
    lambda-uploader -p ./
else
    lambda-uploader -p ./ --profile=$prf
fi
sed -i -e 's/running_local = False/running_local = True/g' $(pwd)/utils/profile.py

echo "Adding cloudwatch rule to the root/master lambda function"
sleep 10

aws lambda add-permission \
--region $reg \
--function-name async-producer-Scheduler \
--statement-id 1 \
--principal events.amazonaws.com \
--action lambda:InvokeFunction \
--source-arn arn:aws:events:$reg:$acc:rule/$rulen \
--profile $prf \
--region $reg


