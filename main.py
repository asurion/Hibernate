from services.ASG import ASG
from asyncProducerUtil.utils.connect import Connect
from validate_tags.validate_master import validate_schedule
import pprint
import datetime
from services.Compute.ec2_autoscaling import AutoScalingDefinition
from services.Compute.ec2_standalone import ElasticComputeDefinition
pp = pprint.PrettyPrinter(indent=1)


def lambda_handler(event, context):

    account = event['account']
    awsregion = event['region']

    customTagName = 'scheduler:sleep'

    # Create connection to the EC2 using Boto3 resources interface
    cxn = Connect(account, awsregion)
    ec2 = cxn.resource_connect('ec2')
    asg_client = cxn.client_connect('autoscaling')

    # Start StopLists
    startList = []
    stopList = []
    asg_startList = []
    asg_stopList = []

    # List all instances
    instances = ec2.instances.filter(
        Filters=[
            {
                'Name': 'tag-key',
                'Values': [
                    'scheduler:sleep', 'SCHEDULER:SLEEP'
                ]
            },
        ]

    )

    print "\nCreating", awsregion, account, "lists..."
    print "Running Standalone EC2 Scheduler"

    for i in instances:

        if i.tags:

            # Ignore the autoscaling instances inside the ec2.all() iteration. Handle autoscaling in diff module
            skip = filter(lambda i: True if 'aws:' in i['Key'] else False, i.tags)

            if skip:
                continue

            for t in i.tags:
                scheduled = validate_schedule(i, t, customTagName)

                if not scheduled:
                    continue

                for s in scheduled:
                    if s.get('start_instance'):
                        startList.append(s)
                    if s.get('stop_instance'):
                        stopList.append(s)

    # EC2 Execute Start and Stop Commands
    if startList:
        print "+++ Starting", len(startList), "instances", startList

        x = []
        for i in startList:
            print "\n[INFO] {} ::: {} ::: {} ::: attempted start @ utc {}".format(customTagName, i['grammar'], i['resource_id'], datetime.datetime.utcnow())
            x.append(i['resource_id'])

        # TODO Log the data somewhere (we only logged data if the instances were 'stopped')
        #flat = ElasticComputeDefinition(account, awsregion).generate_rows(startList)

        ec2.instances.filter(InstanceIds=x).start()

    if stopList:
        print "+++ Stopping", len(stopList), "instances", stopList

        x = []
        for i in stopList:
            print "\n[INFO] {} ::: {} ::: {} ::: attempted stop @ utc {}".format(customTagName, i['grammar'], i['resource_id'], datetime.datetime.utcnow())
            x.append(i['resource_id'])

        ec2.instances.filter(InstanceIds=x).stop()

        # TODO Log the data somewhere (we only logged data if the instances were 'stopped')
        # ec2_log_stopList = [x for x in stopList if x.get('isLogging')]
        #flat = ElasticComputeDefinition(account, awsregion).generate_rows(ec2_log_stopList)

    asg_all = ASG.discover_sleep_tags(asg_client)
    print "\nRunning ASG Scheduler"

    for a in asg_all:
        try:

            asg = ASG(account, awsregion, a['ResourceId'])

            # validate if asg is ready to start or stop
            if asg.tags:
                for t in asg.tags:
                    asg_schedule = validate_schedule(asg, t, customTagName)

                    if not asg_schedule:
                        continue

                    for s in asg_schedule:
                        if s.get('start_instance'):
                            asg_startList.append(s)
                        if s.get('stop_instance'):
                            asg_stopList.append(s)

        except IndexError as indexerror:
            print "[EXCEPTION-IndexError] {}".format(indexerror)

        except KeyError as keyerror:
            print "[EXCEPTION-KeyError] {}".format(keyerror)

        except Exception as e:
            print "[EXCEPTION] for i in asg_all: ... {}".format(e)

    # ASG Execute Start and Stop Commands
    if asg_startList:

        print "+++ Starting", len(asg_startList), "ASG", asg_startList

        for i in asg_startList:
            try:
                print "\n[INFO] {} ::: {} ::: {} ::: attempted start @ utc {}".format(customTagName, i['grammar'], i['resource_id'], datetime.datetime.utcnow())
                asg = ASG(account, awsregion, i['resource_id'])
                min_max_desired_tag = asg.get_config_tag()

                asg.wake_auto_scaling_group(min_max_desired_tag)
            except Exception as e:
                print "[EXCEPTION] for i in asg_startList: ... {}".format(e)

        # TODO Log the data somewhere (we only logged data if the instances were 'stopped')
        # flat = AutoScalingDefinition(account, awsregion).generate_rows(asg_log_stopList)

    if asg_stopList:
        print "+++ Stopping", len(asg_stopList), "ASG", asg_stopList

        for i in asg_stopList:
            try:
                print "\n[INFO] {} ::: {} ::: {} ::: attempted stop @ utc {}".format(customTagName, i['grammar'], i['resource_id'], datetime.datetime.utcnow())
                asg = ASG(account, awsregion, i['resource_id'])
                min_max_desired_tag = asg.get_config_tag()
                print min_max_desired_tag
                current_min_max_desired = asg.minSize, asg.maxSize, asg.desiredCapacity

                if min_max_desired_tag is None:
                    asg.put_previous_config_tag(current_min_max_desired)

                if min_max_desired_tag != current_min_max_desired:
                    asg.put_previous_config_tag(current_min_max_desired)

                asg.sleep_auto_scaling_group()
            except Exception as e:
                print "[EXCEPTION] for i in asg_stopList: ... {}".format(e)

        # TODO Log the data somewhere (we only logged data if the instances were 'stopped')
        # asg_log_stopList = [x for x in asg_stopList if x.get('isLogging')]
        #flat = AutoScalingDefinition(account, awsregion).generate_rows(asg_log_stopList)


if __name__ == '__main__':

    lambda_handler({'account':'SQA', 'region': 'us-east-1'}, '')
