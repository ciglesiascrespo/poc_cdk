#!/usr/bin/env python3
import os

import aws_cdk as cdk


#from cdk_project.cdk_project_stack import CdkProjectStack
#from serverless_stacks.custom_lambda import CustomLambdaStack
#from serverless_stacks.custom_lambda_src_from_s3 import CustomLambdaSrcFromS3Stack
from poc_project.stacks.poc_stack import PocStack

app = cdk.App()
# CdkProjectStack(app, "CdkProjectStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#    )

PocStack(app,"POCProject",
     description="Create Serverless Event Processor using Lambda")
app.synth()
