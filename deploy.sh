#!/bin/bash

account_number=$(cat config.json | jq .MASTER_ACCOUNT_NUMBER)
profile=$(cat config.json | jq .PROFILE)
region=$(cat config.json | jq .REGION)
role=$(cat config.json | jq .MASTER_ROLE_NAME)

reg=$(echo $"$region" | tr -d '"')
acc=$(echo $"$account_number" | tr -d '"')
r=$(echo $"$role" | tr -d '"')
prf=$(echo $"$profile" | tr -d '"')

new_role=arn:aws:iam::$acc:role/$r
echo $reg
echo $new_role

sed -i -e "s/running_local = True/running_local = False/g" $(pwd)/asyncProducerUtil/utils/profile.py
sed -i -e "s/REGION/$reg/g" $(pwd)/lambda.json
sed -i -e "s@ROLE@$new_role@g" $(pwd)/lambda.json


if [ ! -f ~/.aws/credentials ]; then
    lambda-uploader -p ./
else
    lambda-uploader -p ./ --profile=$prf
fi
sed -i -e 's/running_local = False/running_local = True/g' $(pwd)/asyncProducerUtil/utils/profile.py




