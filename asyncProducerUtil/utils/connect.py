import boto3
from profile import running_local, local_profile, role_title
from accounts_meta import account_names_iterable, get_account_num_from_name, \
    get_account_name_from_num, account_numbers_iterable

from config import LEAF_ROLE_NAME, MASTER_ROLE_NAME
class Connect:

    def __init__(self, account, region):

        self.account = account
        self.region = region

        if account.isdigit():
            self.account = self.account_name

        if account == 'GOV':
            self.role_arn = 'arn:aws:iam::{}:role/{}'.format(self.account_number, MASTER_ROLE_NAME)
        else:
            self.role_arn = 'arn:aws:iam::{}:role/{}'.format(self.account_number, LEAF_ROLE_NAME)

        if running_local:
            sts = boto3.Session(profile_name=local_profile).client('sts')
        else:
            sts = boto3.client('sts')

        self.role = sts.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName='{}-{}'.format(role_title, self.account)
        )

        self.session = boto3.Session(
            aws_access_key_id=self.role['Credentials']['AccessKeyId'],
            aws_secret_access_key=self.role['Credentials']['SecretAccessKey'],
            aws_session_token=self.role['Credentials']['SessionToken'],
            region_name=self.region
        )

    def client_connect(self, service_name):
        return self.session.client(service_name)

    def resource_connect(self, service_name):
        return self.session.resource(service_name)

    @property
    def account_number(self):
        return get_account_num_from_name(self.account)

    @property
    def account_name(self):
        return get_account_name_from_num(self.account)

    def get_all_regions(self):
        return self.session.get_available_regions('ec2')

    def get_regions(self, service_name):
        return self.session.get_available_regions(service_name)




