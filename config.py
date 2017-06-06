import json

with open('config.json') as data_file:
    config_data = json.load(data_file)

MASTER_ROLE_NAME = config_data['MASTER_ROLE_NAME']
MASTER_ACCOUNT_NUMBER = config_data['MASTER_ACCOUNT_NUMBER']
LEAF_ROLE_NAME = config_data['LEAF_ROLE_NAME']
LEAF_ACCOUNT_NUMBER = config_data['LEAF_ACCOUNT_NUMBER']
PROFILE = config_data['PROFILE']
TABLE_NAME = config_data['TABLE_NAME']
REGION = config_data['REGION']
CW_RULE_NAME = config_data['CW_RULE_NAME']

