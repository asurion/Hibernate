from asyncProducerUtil.utils.connect import Connect


class ASG(Connect):
    api_name = 'autoscaling'

    def __init__(self, account, region, asg_name):
        self.asg_name = asg_name

        Connect.__init__(self, account, region)

        self.client = Connect.client_connect(self, self.api_name)
        self.ec2_client = Connect.client_connect(self, 'ec2')
        self.ec2_resource = Connect.resource_connect(self, 'ec2')
        print "[ASG-LOG] {}".format(self.asg_name)

        self.describeOnce = self.client.describe_auto_scaling_groups(AutoScalingGroupNames=[self.asg_name])['AutoScalingGroups'][0]

        lc = self.describeOnce['LaunchConfigurationName']

        self.describe_lc = self.client.describe_launch_configurations(LaunchConfigurationNames=[lc])['LaunchConfigurations'][0]

    def get_instances(self):
        return self.describeOnce['Instances']

    def get_config_tag(self):

        response = self.client.describe_tags(
            Filters=[
                {
                    'Name': 'auto-scaling-group',
                    'Values': [
                        self.asg_name,
                    ]
                },
            ]
        )

        config_tags = next(
            (item for item in response['Tags'] if item["Key"] == "scheduler:asg-previous:min,max,desired"), None)
        if config_tags:
            cf = config_tags['Value']
            tmp = cf.split(';')
            cf = int(tmp[0]), int(tmp[1]), int(tmp[2])
        else:
            cf = None

        return cf

    def put_previous_config_tag(self, prev):

        min = prev[0]
        max = prev[1]
        desired = prev[2]
        self.client.create_or_update_tags(
            Tags=[
                {
                    'ResourceId': self.asg_name,
                    'ResourceType': 'auto-scaling-group',
                    'Key': 'scheduler:asg-previous:min,max,desired',
                    'Value': '{};{};{}'.format(min, max, desired),
                    'PropagateAtLaunch': True
                },
            ]
        )

    def wake_auto_scaling_group(self, asg_previous_tag):

        minsize = asg_previous_tag[0]
        maxsize = asg_previous_tag[1]
        desired = asg_previous_tag[2]

        self.client.update_auto_scaling_group(
            AutoScalingGroupName=self.asg_name,
            MaxSize=int(maxsize),
            MinSize=int(minsize),
            DesiredCapacity=int(desired)
        )

    def sleep_auto_scaling_group(self):
        self.client.update_auto_scaling_group(
            AutoScalingGroupName=self.asg_name,
            MinSize=0,
            DesiredCapacity=0
        )

    @staticmethod
    def discover_sleep_tags(client):

        paginator = client.get_paginator('describe_tags')
        response_iterator = paginator.paginate(
            Filters=[
                {
                    'Name': 'key',
                    'Values': [
                        'scheduler:sleep', 'SCHEDULER:SLEEP'
                    ]
                },
            ],

        )
        z = []
        for r in response_iterator:
            z.extend(r['Tags'])

        good = [g for g in z if not g['Value'].lower() in ['inactive', 'alternative']]

        # list of Auto Scaling Groups that have the scheduler:sleep tag
        return good

    @property
    def arn(self):
        return self.describeOnce['AutoScalingGroupARN']

    @property
    def id(self):
        return self.describeOnce['AutoScalingGroupName']

    @property
    def name(self):
        return self.describeOnce['AutoScalingGroupName']

    @property
    def tags(self):
        return self.describeOnce['Tags']

    @property
    def minSize(self):
        return self.describeOnce['MinSize']

    @property
    def maxSize(self):
        return self.describeOnce['MaxSize']

    @property
    def desiredCapacity(self):
        return self.describeOnce['DesiredCapacity']

    @property
    def state(self):
        state = self.describeOnce['DesiredCapacity']
        if state == 0:
            state = 'stopped'
        elif state >= 1:
            state = 'running'

        return {'Name': state}


    @property
    def VPCZoneIdentifier(self):
        return self.describeOnce['VPCZoneIdentifier']

    @property
    def LaunchConfigurationName(self):
        return self.describeOnce['LaunchConfigurationName']

    @property
    def lc(self):
        return self.describe_lc

    @property
    def instance_type(self):
        return self.describe_lc['InstanceType']

    @property
    def num_instances(self):
        return len(self.get_instances())

    @property
    def tenancy(self):
        t = self.describe_lc.get('PlacementTenancy')
        if t is None:
            t = 'default'

        return t

    @property
    def operating_system(self):
        instance_id = self.describeOnce['Instances'][0]['InstanceId']
        i = self.ec2_resource.Instance(instance_id)
        return i.platform



