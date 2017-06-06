from asyncProducerUtil.utils.connect import Connect
from utils.tenancy import get_ec2_tenancy


def putCloudWatchMetric(account, region, instance, instance_state, platform):
    _boto3_ = Connect('GOV', 'us-east-1')
    cw = _boto3_.client_connect('cloudwatch')
    tenancy = get_ec2_tenancy(client=Connect(account, region).client_connect('ec2'), instance_id=instance.id)
    if platform is None:
        platform = 'NotAvailable'


    cw.put_metric_data(
        Namespace='EC2Scheduler',
        MetricData=[{
            'MetricName': instance.id,
            'Value': instance_state,

            'Unit': 'Count',
            'Dimensions': [
                {
                    'Name': 'Region',
                    'Value': region
                },
                {
                    'Name': 'Account',
                    'Value': account
                },
                {
                    'Name': 'instance_type',
                    'Value': instance.instance_type
                },
                {
                    'Name': 'Platform',
                    'Value': platform
                },
                {
                    'Name': 'Tenancy',
                    'Value': tenancy
                }
            ]
        }]

    )


def putCloudWatchMetricASG(asg, asg_state, platform):
    _boto3_ = Connect('GOV', 'us-east-1')
    cw = _boto3_.client_connect('cloudwatch')


    if platform is None:
        platform = 'NotAvailable'


    cw.put_metric_data(
        Namespace='EC2Scheduler-ASG',
        MetricData=[{
            'MetricName': asg.id,
            'Value': asg_state,

            'Unit': 'Count',
            'Dimensions': [
                {
                    'Name': 'Region',
                    'Value': asg.region
                },
                {
                    'Name': 'Account',
                    'Value': asg.account
                },
                {
                    'Name': 'instance_type',
                    'Value': asg.instance_type
                },
                {
                    'Name': 'Platform',
                    'Value': platform
                },
                {
                    'Name': 'Tenancy',
                    'Value': asg.tenancy
                }
                # {
                #     'Name': 'Num_instances',
                #     'Value': str(asg.num_instances)
                # },

            ]
        }]

    )