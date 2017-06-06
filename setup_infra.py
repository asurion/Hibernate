import json
from boto3.session import Session
from botocore.exceptions import ClientError
import boto3
from urllib2 import Request, urlopen, URLError
from config import TABLE_NAME, LEAF_ROLE_NAME, MASTER_ROLE_NAME, PROFILE, LEAF_ACCOUNT_NUMBER, MASTER_ACCOUNT_NUMBER, REGION, CW_RULE_NAME
from time import sleep

def allow_master_to_assume():
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "assume1",
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }


# allows master_role to assumed leaf_role
# also use this role so master can assume itself
def default_trust(account_number):
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            },
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::" + account_number + ":root"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }


# leaf_role will be assumed by master_role
def create_role(session, role_name, account_number):

    client = session.client('iam')
    res = None

    try:
        role = client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(default_trust(str(account_number)))
        )

        client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
        )

        res = role['Role']['Arn']

        print "+ Created IAM role: {}".format(res)

    except ClientError as e:
        raise e


    return res


def build_table(session, table_name, account_data):

    client = session.client('dynamodb')
    try:
        t = client.create_table(TableName=table_name,
                            KeySchema=[
                                {
                                    'AttributeName': 'name',
                                    'KeyType': 'HASH'
                                }
                            ],
                            AttributeDefinitions=[
                                {
                                    'AttributeName': 'name',
                                    'AttributeType': 'S'
                                }
                            ],
                            ProvisionedThroughput={
                                'ReadCapacityUnits': 10,
                                'WriteCapacityUnits': 1
                            },
                            )

        resource = session.resource('dynamodb')

        print "+ Created Dynamodb Table: {}... Waiting for table creation to propagate before inserting items".format(table_name)
        sleep(15)

        table = resource.Table(table_name)
        for i in account_data:
            table.put_item(Item=i)

    except ClientError as e:
        raise e

    return t['TableDescription']['TableName']


def create_cw_event_trigger(session):
    client = session.client('dynamodb')
    rule_arn = []
    try:
        response = client.put_rule(
            Name='{}'.format(CW_RULE_NAME),
            ScheduleExpression='cron(0/10 * * * ? *)',
            Description='schedule ec2 lamabda function to run every 10 minutes.'
        )

        rule_arn = response['RuleArn']
        print "+ Created Cloud Watch Rule: ".format(rule_arn)

    except Exception as e:
        raise e

    return rule_arn


def access_session(profile, region):

    try:
        locality_check = Request('http://169.254.169.254/latest/meta-data/')
        urlopen(locality_check)
        on_ec2 = True
    except URLError:
        on_ec2 = False

    if on_ec2:
        client = boto3
    else:
        client = Session(profile_name=profile, region_name=region)

    return client


def scheduler_sleep():

    masteraccount_profile = PROFILE
    region = REGION
    master_account_number = MASTER_ACCOUNT_NUMBER
    dynamo_table_name = TABLE_NAME
    master_role = MASTER_ROLE_NAME
    leaf_role = LEAF_ROLE_NAME
    leaf_account_number = LEAF_ACCOUNT_NUMBER

    accountdata = [
        {
            'name': 'GOV',
            'account_number': master_account_number
        },
        {
            'name': 'ACCOUNT2',
            'account_number': leaf_account_number
        }
    ]

    sesh = access_session(masteraccount_profile, region)

    build_table(sesh, dynamo_table_name, accountdata)
    create_role(sesh, master_role, master_account_number)
    create_cw_event_trigger(sesh)

    # deploy 2 functions
    print "Time to deploy the lambda functions in the rootnode account. See next steps."


if __name__ == '__main__':
    scheduler_sleep()





