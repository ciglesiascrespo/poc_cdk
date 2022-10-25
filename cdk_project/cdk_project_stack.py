from constructs import Construct
from aws_cdk import App, Stack                    # core constructs
from aws_cdk import aws_s3 as S3

class CdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        S3.Bucket(
            self,
            "myBucketId",
            bucket_name = "test-s3-cdk-ci",
            access_control = S3.BucketAccessControl.PRIVATE,
            encryption = S3.BucketEncryption.S3_MANAGED,
            versioned = False,
            block_public_access = S3.BlockPublicAccess.BLOCK_ALL
        )