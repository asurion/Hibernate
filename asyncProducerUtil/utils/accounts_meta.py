import boto3
from profile import running_local, local_profile
from config import TABLE_NAME
region = 'us-east-1'


def accounts_meta_iterable():

    if running_local:
        s = boto3.Session(profile_name=local_profile, region_name=region)
        dynamodb = s.resource('dynamodb')
    else:
        dynamodb = boto3.resource('dynamodb', region_name=region)

    table = dynamodb.Table(TABLE_NAME)
    return table.scan()['Items']


def get_account_name_from_num(account_name):
    for acc in accounts_meta_iterable():
        if acc['account_number'] == account_name:
            return acc['name']


def get_account_num_from_name(account_name):
    for acc in accounts_meta_iterable():
        if acc['name'] == account_name:
            return acc['account_number']


def account_names_iterable():
    return [acc['name'] for acc in accounts_meta_iterable()]


def account_numbers_iterable():
    return [acc['account_number'] for acc in accounts_meta_iterable()]