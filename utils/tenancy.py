

def get_ec2_tenancy(client, instance_id):
    return client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['Placement']['Tenancy']

