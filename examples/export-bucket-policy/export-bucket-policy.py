import os

from awacs.aws import Policy, Statement, Action, Principal
from troposphere import Sub, Template, Join
from troposphere.s3 import BucketPolicy

t = Template()
t.set_version('2010-09-09')

current_file_name = os.path.splitext(os.path.basename(__file__))[0]

"""
Replace 'my-s3-bucket-* with the correct values
"""
export_bucket_policy = t.add_resource(BucketPolicy(
    'ExportBucketPolicy',
    Bucket='my-s3-bucket-name',
    PolicyDocument=Policy(
        Statement=[
            Statement(
                Effect='Allow',
                Action=[
                    Action('s3', 'GetBucketAcl')
                ],
                Principal=Principal(
                    'Service',
                    Sub('logs.${AWS::Region}.amazonaws.com')
                ),
                Resource=[
                    'my-s3-bucket-arn'
                ],
            ),
            Statement(
                Effect='Allow',
                Action=[
                    Action('s3', 'PutObject')
                ],
                Principal=Principal(
                    'Service',
                    Sub('logs.${AWS::Region}.amazonaws.com')
                ),
                Resource=[
                    Join('/', ['my-s3-bucket-arn', '*'])
                ],
            )
        ]
    )
))

print(t.to_json(), file=open('{0}.json'.format(current_file_name), 'w'))
print(t.to_yaml(), file=open('{0}.yaml'.format(current_file_name), 'w'))
