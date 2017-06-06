from utils.randomGen import generateRandomString
from asyncProducerUtil.utils.connect import Connect
from services.ASG import ASG


class AutoScalingDefinition(Connect):

    api_name = 'auto-scaling'
    table_name = 'scheduler_state_logs'

    def asg_def(self, asg, schedule):

        OS = asg.operating_system
        if OS is None:
            OS = 'linux'

        tenancy = asg.tenancy
        if tenancy == 'default':
            tenancy = 'shared'

        PLATFORM = []
        BUSINESS_UNIT = []
        p = next((item for item in asg.tags if item["Key"] == "PLATFORM"), None)
        if p: PLATFORM = p['Value']
        b = next((item for item in asg.tags if item["Key"] == "BUSINESS_UNIT"), None)
        if b: BUSINESS_UNIT = b['Value']

        if isinstance(schedule.get('daysActive'), list):
            daysActive = ','.join(schedule.get('daysActive'))
        else:
            daysActive = schedule.get('daysActive')

        return {
            "uuid": generateRandomString(16),
            "resource_id": asg.id,
            "resource_type": "asg",
            "Region": asg.region,
            "Account": self.account,
            "InstanceType": asg.instance_type,
            "OperatingSystem": OS,
            "Tenancy": tenancy,
            "PLATFORM": PLATFORM,
            "BUSINESS_UNIT": BUSINESS_UNIT,
            "StopTime": int(schedule.get('stop_time')),
            "StartTime": int(schedule.get('start_time')),
            "instance_count": asg.num_instances,
            "schedule": daysActive,
            "tz": schedule.get('tz'),
            "TotalHours": schedule.get('TotalHours') * asg.num_instances
        }

    def __init__(self, account, region):
        Connect.__init__(self, account, region)

        # self.resource = Connect.resource_connect(self, self.api_name)

    def generate_rows(self, schedules):

        auto_scaling_groups = []

        for s in schedules:

            asg = ASG(self.account, self.region, s['resource_id'])
            try:
                asg_table_row = self.asg_def(asg, s)
                auto_scaling_groups.append(asg_table_row)
            except Exception as e:
                print e

        return {
            self.table_name: auto_scaling_groups
        }
