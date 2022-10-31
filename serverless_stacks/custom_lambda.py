from constructs import Construct
from aws_cdk import Stack, CfnOutput               # core constructs
from aws_cdk import aws_lambda 

class CustomLambdaStack(Stack):

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
                                          #timeout=core .Duration.seconds(3),
                                          environment={
                                              'LOG_LEVEL':'INFO'
                                          }
                                          )
