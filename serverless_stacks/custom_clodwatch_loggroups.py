from constructs import Construct
from aws_cdk import Stack, Duration  , RemovalPolicy             # core constructs
from aws_cdk import aws_lambda 
from aws_cdk import aws_logs as logs

class CustomLambdaLogsGroupStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        try:
            with open('serverless_stacks/lambda_src/konston_processor.py',mode='r') as f:
                konstone_fn_code = f.read()
        except OSError:
            print('Unable to read lambda function code')
        
        
        konstone_fn = aws_lambda.Function(self,
                                          "konstoneFunctionId",
                                          function_name="konstone_function",
                                          runtime=aws_lambda.Runtime.PYTHON_3_7,
                                          handler="index.lambda_handler",
                                          code=aws_lambda.InlineCode(konstone_fn_code),
                                          timeout=Duration.seconds(3),
                                          environment={
                                              'LOG_LEVEL':'INFO'
                                          }
                                          )
        # Create Custom logGroup
        # /aws/lambda/funciont-name
        konstone_log = logs.LogGroup(self,"konstoneLogGroup",
                                     log_group_name=f"/aws/lambda/{konstone_fn.function_name}",
                                     removal_policy=RemovalPolicy.DESTROY)