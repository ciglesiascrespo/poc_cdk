from cgitb import handler
from constructs import Construct
from aws_cdk import Stack, aws_dynamodb as DB, aws_s3 as S3, aws_iam as IAM, aws_apigateway as API
from aws_cdk import RemovalPolicy, CfnOutput
from poc_project.constructs.lambda_custom import LambdaCustom


class PocStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create Bucket Logs 
        bucket_logs = S3.Bucket(
            self,
            "myBucketId",
            bucket_name = "test-s3-cdk-ci",
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # create table in DynamoDB
        logs_table = DB.Table(
            self,
            "LogsDBTable",
            table_name="logs-table",
            partition_key=DB.Attribute(
                name="file_name",
                type=DB.AttributeType.STRING,
            ),
            removal_policy=RemovalPolicy.DESTROY
        )
        
        #### Lambda Read Bucket
        lambda_read_bucket = LambdaCustom(self,"LambdaReadBucketId",
                                 'poc_project/lambda_src/lambda_src_get_bucket.py',
                                 "poc_function_read_bucket",
                                 {
                                    'LOG_LEVEL':'INFO',
                                    "DDB_TABLE_NAME": f"{logs_table.table_name}",
                                    "BUCKET_LOGS_NAME":f"{bucket_logs.bucket_name}"
                                  }).lambda_fn
        
        # Add permisiion to read S3 bucket logs
        bucket_logs.grant_read(lambda_read_bucket)
        
        # Add permission to rite to DynamoDb
        logs_table.grant_write_data(lambda_read_bucket)
        
        #### Lambda Read Logs
        lambda_read_logs = LambdaCustom(self,"LambdaReadLogsId",
                                 'poc_project/lambda_src/lambda_src_get_logs.py',
                                 "poc_function_read_logs",
                                 {
                                    'LOG_LEVEL':'INFO',
                                    'LOG_GROUP_NAME':f'/aws/lambda/{lambda_read_bucket.function_name}',
                                    "DDB_TABLE_NAME": f"{logs_table.table_name}",
                                    "BUCKET_LOGS_NAME":f"{bucket_logs.bucket_name}"
                                  }).lambda_fn
        # Add permission to read logs
        lambda_read_logs.role.add_managed_policy(
            IAM.ManagedPolicy.from_aws_managed_policy_name('CloudWatchLogsFullAccess')
        )
        # Add permisiion to read S3 bucket logs
        bucket_logs.grant_write(lambda_read_logs)
        

        # Add Api GTW endpoiint to lambda
        apiGtw = API.RestApi(self,"ApiUrl",
                          rest_api_name="Rest Api POC CDK",
                          description="This Rest Api get logs and S3 buckets"
                          )
        
        # Add endpoint GET logs
        getLogsIntegration = API.LambdaIntegration(lambda_read_logs)
        logs = apiGtw.root.add_resource("logs")
        logs.add_method("GET",getLogsIntegration)
        
        # Add endpoint GET buckets
        getBucketsIntegration = API.LambdaIntegration(lambda_read_bucket)
        buckets = apiGtw.root.add_resource("buckets");
        buckets.add_method("GET",getBucketsIntegration)
        
        # print the IAM role arn for this service account
        CfnOutput(self, "Endpoint Api", value=apiGtw.url)