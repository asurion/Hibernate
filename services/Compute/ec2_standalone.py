from utils.randomGen import generateRandomString
from asyncProducerUtil.utils.connect import Connect


class ElasticComputeDefinition(Connect):

    api_name = 'ec2'
    table_name = 'scheduler_state_logs'

    def ec2_def(self, i, schedule):

        OS = i.platform
        if OS is None:
            OS = 'linux'

        tenancy = i.placement['Tenancy']
        if tenancy =='default':
            tenancy = 'shared'

        PLATFORM = []
        BUSINESS_UNIT = []
        p = next((item for item in i.tags if item["Key"] == "PLATFORM"), None)
        if p: PLATFORM = p['Value']
        b = next((item for item in i.tags if item["Key"] == "BUSINESS_UNIT"), None)
        if b: BUSINESS_UNIT = b['Value']

        if isinstance(schedule.get('daysActive'), list):
            daysActive = ','.join(schedule.get('daysActive'))
        else:
            daysActive = schedule.get('daysActive')


        return {
                "uuid": generateRandomString(16),
                "resource_id": i.instance_id,
                "Account": self.account,
                "resource_type": "ec2",
                "Region": self.region,
                "InstanceType": i.instance_type,
                "OperatingSystem": OS,
                "Tenancy": tenancy,
                "PLATFORM": PLATFORM,
                "BUSINESS_UNIT": BUSINESS_UNIT,
                "StopTime": int(schedule.get('stop_time')),
                "StartTime": int(schedule.get('start_time')),
                "instance_count": 1,
                "schedule": daysActive,
                "tz": schedule.get('tz'),
                "TotalHours": schedule.get('TotalHours')
        }

    def __init__(self, account, region):
        Connect.__init__(self, account, region)

        self.resource = Connect.resource_connect(self, self.api_name)

    def generate_rows(self, schedules):

        ec2_instances = []

        for s in schedules:

            i = self.resource.Instance(s['resource_id'])
            try:
                ec2_table_row = self.ec2_def(i, s)
                ec2_instances.append(ec2_table_row)
            except Exception as e:
                print e


        return {
            self.table_name: ec2_instances
        }