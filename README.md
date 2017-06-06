# Multi account EC2 Sleep Scheduler

[You should see the tagging language before getting started](../browse/tag_grammar.md)



### step 1: (manually) create new slave/leaf role in the target account(s)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::{master_account_number}:root" 
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```
#### add inline policy permissions 
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "permissions",
            "Effect": "Allow",
            "Action": [
                "ec2:*,
                "autoscaling:*",
                "dynamodb:*",
                "lambda:*",
                "logs:*"
                ],
            "Resource": "*"
        }
    ]
}
```



### step 2: Edit config.json and deploy
for demonstration purposes, we only need to setup this script with 2 accounts, 1 master 1 slave.
to add more accounts, simply add a new item to the 'accounts-metadata' dynamodb table post build.

```
python setup_infra.py
```

## TEST.
 At this point you can test without uploading the lambda functions to your AWS account.
 Simply edit the account variable in main.py. (must exist in the dynamo table you just deployed)
 Testing a single account, single region. You will need a SCHEDULER:SLEEP tag on one of your instances in the target account.
 Run the program.

```python
if __name__ == '__main__':

    lambda_handler({'account':'ACCOUNT1', 'region': 'us-east-1'}, '')

```


### step 3: Deploy the 2 lambda functions

There are 2 lambda functions. We will deploy using a package called lambda-uploader

The first lambda function is the master function which will instantiate a new instance of the scheduler_sleep worker function in each account and region

Example snippet
```python
for a in account_names_iterable():
    for region in x.get_all_regions():

        response = client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:{}:function:async-worker-Scheduler',
            InvocationType='Event',
            Payload=json.dumps({
                'account': a,
                'region': region
            })
        )
```

##### Function 1
```
cd asyncProducerUtil
./deploy.sh
```
##### Function 2
```
cd ..
./deploy.sh
```

Simply add new items to the accounts-metadata dynamodb table to encompass those accounts and begin scheduling those instances to sleep.
