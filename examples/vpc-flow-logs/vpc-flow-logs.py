import os

from awacs.aws import Statement, Action, Principal, PolicyDocument
from troposphere import Template
from troposphere.iam import Role, Policy

t = Template()
t.set_version('2010-09-09')

current_file_name = os.path.splitext(os.path.basename(__file__))[0]

vpc_flow_logs = t.add_resource(Role(
    "VPCFlowLogsRole",
    AssumeRolePolicyDocument={
        'Statement': [
            Statement(
                Action=[Action('sts', 'AssumeRole')],
                Effect='Allow',
                Principal=Principal(
                    'Service',
                    [
                        'vpc-flow-logs.amazonaws.com'
                    ]
                )
            )
        ],
        'Version': '2012-10-17'
    },
    Policies=[
        Policy(
            PolicyName='VPCFlowLogsPolicy',
            PolicyDocument=PolicyDocument(
                Statement=[
                    Statement(
                        Action=[
                            Action('logs', 'CreateLogGroup'),
                            Action('logs', 'CreateLogStream'),
                            Action('logs', 'DescribeLogGroups'),
                            Action('logs', 'DescribeLogStreams'),
                            Action('logs', 'PutLogEvents')
                        ],
                        Effect='Allow',
                        Resource=['*'],
                        Sid='CloudWatchPermissions'
                    )
                ],
                Version='2012-10-17'
            )
        )
    ],
    RoleName='vpc-flow-logs-role',
))

print(t.to_json(), file=open('{0}.json'.format(current_file_name), 'w'))
print(t.to_yaml(), file=open('{0}.yaml'.format(current_file_name), 'w'))
