from constructs import Construct
from aws_cdk import App, Stack, CfnOutput                    # core constructs
from aws_cdk import aws_s3 as S3

class CdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        print(self.node.try_get_context('prod'))
        myS3 = S3.Bucket(
            self,
            "myBucketId",
            bucket_name = "test-s3-cdk-ci",
            access_control = S3.BucketAccessControl.PRIVATE,
            encryption = S3.BucketEncryption.S3_MANAGED,
            versioned = False,
            block_public_access = S3.BlockPublicAccess.BLOCK_ALL
        )
        
        # print the IAM role arn for this service account
        CfnOutput(self, "S3Name", value=myS3.bucket_name)
        
        