from constructs import Construct
from aws_cdk import  Duration, aws_lambda

class LambdaCustom(Construct):

    def __init__(self, scope: Construct, construct_id: str,code_path:str,fn_name:str,env_var ,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)       
        
        # Read code for lambda get bucket
        try:
            with open(f'{code_path}',mode='r') as f:
                lambda_fn_code = f.read()
        except OSError:
            print('Unable to read lambda function code')
        
        # create lambda function
        self.lambda_fn = aws_lambda.Function(self,
                                          f"{fn_name}Id",
                                          function_name=f"{fn_name}",
                                          runtime=aws_lambda.Runtime.PYTHON_3_7,
                                          handler="index.lambda_handler",
                                          code=aws_lambda.InlineCode(lambda_fn_code),
                                          timeout=Duration.minutes(3),
                                          environment=env_var
                                          )