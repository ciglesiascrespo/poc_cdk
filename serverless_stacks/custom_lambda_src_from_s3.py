from ast import Lambda
from constructs import Construct
from aws_cdk import Duration, Stack, RemovalPolicy               # core constructs
from aws_cdk import aws_lambda as Lambda, aws_s3 as S3, aws_logs as Logs

class CustomLambdaSrcFromS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
              
        
        # Import lambda source from S3 Bucket
        konstone_bkt = S3.Bucket.from_bucket_attributes(self,"konstoneAssetsBucket",bucket_name="test-s3-cdk-ci")
        
        # Create Lambda function
        
        konstone_fn = Lambda.Function(self,"konstoneFn",
                                     function_name="konstone_function_s3",
                                     runtime=Lambda.Runtime.PYTHON_3_7,
                                     timeout=Duration.seconds(3),
                                     code=Lambda.S3Code(konstone_bkt,"konstone_processor.zip"),
                                     handler="konstone_processor.lambda_handler")
        # Creat Logs Groups
        konstone_logs = Logs.LogGroup(self, "konstoneLogGroup",
                                      log_group_name=f"/aws/lambda/{konstone_fn.function_name}",
                                      removal_policy=RemovalPolicy.DESTROY,
                                      retention=Logs.RetentionDays.ONE_WEEK)
        
