from utils.connect import Connect
from utils.accounts_meta import account_names_iterable
import json
from config import MASTER_ACCOUNT_NUMBER, REGION


def lambda_handler(event, context):

    x = Connect('GOV', 'us-east-1')
    client = x.client_connect('lambda')

    for a in account_names_iterable():
        for region in x.get_all_regions():

            response = client.invoke(
                FunctionName='arn:aws:lambda:{}:{}:function:async-worker-Scheduler'.format(REGION, MASTER_ACCOUNT_NUMBER),
                InvocationType='Event',
                Payload=json.dumps({
                    'account': a,
                    'region': region
                })
            )


#lambda_handler('schedule', '')
