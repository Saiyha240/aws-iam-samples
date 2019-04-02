About
=====

Sample IAM Roles and Policies for different services in AWS.

Written using [troposphere](https://github.com/cloudtools/troposphere) and generates AWS CloudFormation JSON and YAML files when executed


Installation
============

awacs can be installed using the pip distribution system for python by
issuing:

```bash
$ pip install -r requirements.txt
```

Examples
========
Some files require you to modify texts that correspond to your services before executing the Python file

Generating Export Bucket Policy for use with AWS CloudWatch Logs Export

Replace `my-s3-bucket-name` and `my-s3-bucket-arn` with your own information:

```python
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
```

Execute to produce JSON and YAML files:

```bash
python export-bucket-policy/export-bucket-policy.py 
```

Generated JSON file:

```json
{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "ExportBucketPolicy": {
            "Properties": {
                "Bucket": "my-s3-bucket-name",
                "PolicyDocument": {
                    "Statement": [
                        {
                            "Action": [
                                "s3:GetBucketAcl"
                            ],
                            "Effect": "Allow",
                            "Principal": {
                                "Service": {
                                    "Fn::Sub": "logs.${AWS::Region}.amazonaws.com"
                                }
                            },
                            "Resource": [
                                "my-s3-bucket-arn"
                            ]
                        },
                        {
                            "Action": [
                                "s3:PutObject"
                            ],
                            "Effect": "Allow",
                            "Principal": {
                                "Service": {
                                    "Fn::Sub": "logs.${AWS::Region}.amazonaws.com"
                                }
                            },
                            "Resource": [
                                {
                                    "Fn::Join": [
                                        "/",
                                        [
                                            "my-s3-bucket-arn",
                                            "*"
                                        ]
                                    ]
                                }
                            ]
                        }
                    ]
                }
            },
            "Type": "AWS::S3::BucketPolicy"
        }
    }
}
```

Generated YAML file:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  ExportBucketPolicy:
    Properties:
      Bucket: my-s3-bucket-name
      PolicyDocument:
        Statement:
          - Action:
              - s3:GetBucketAcl
            Effect: Allow
            Principal:
              Service: !Sub 'logs.${AWS::Region}.amazonaws.com'
            Resource:
              - my-s3-bucket-arn
          - Action:
              - s3:PutObject
            Effect: Allow
            Principal:
              Service: !Sub 'logs.${AWS::Region}.amazonaws.com'
            Resource:
              - !Join
                - /
                - - my-s3-bucket-arn
                  - '*'
    Type: AWS::S3::BucketPolicy
```