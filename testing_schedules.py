# from asyncProducerUtil.utils.connect import Connect
#
#
# def add_tags(client_, instance_id, schedule_tag):
#
#     response = client_.create_tags(
#         Resources=[
#             instance_id,
#         ],
#         Tags=[
#             {
#                 'Key': 'scheduler:sleep',
#                 'Value': schedule_tag
#             },
#             {
#                 'Key':'BUSINESS_UNIT',
#                 'Value': 'OPERATIONS'
#             },
#             {
#                 'Key': 'PLATFORM',
#                 'Value': 'GOV'
#             },
#             {
#                 'Key': 'CLIENT',
#                 'Value': 'ALL'
#             },
#             {
#                 'Key': 'BUSINESS_REGION',
#                 'Value': 'GLOBAL'
#             },
#             {
#                 'Key': 'Name',
#                 'Value': schedule_tag
#             }
#         ]
#     )
#
# #
# # schedules= ['followthesun', '1200;0600;ct;weekends', '1600;0700;ct;weekdays', '1600;1200;ct;all']
# #
# # cxn = Connect('POC', 'us-east-1')
# #
# # client = cxn.client_connect('ec2')
#
#
# def run_instance():
#     response = client.run_instances(
#         ImageId='ami-9be6f38c',
#         MinCount=1,
#         MaxCount=1,
#         InstanceType='t2.micro'
#     )
#     return response['Instances'][0]['InstanceId']
#
# # for sched in schedules:
# #     i_id = run_instance()
# #     add_tags(client, i_id, sched)
#
