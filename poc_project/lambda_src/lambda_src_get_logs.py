# -*- coding: utf-8 -*-

import boto3
import json
import logging
import os

_s3_client = boto3.client('s3')
_logs = boto3.client('logs')


def _bkt_put_item(item):
    """ Insert Item into Bucket S3 """
    
    
    if os.environ.get('BUCKET_LOGS_NAME'):
        bucket_name = os.environ.get('BUCKET_LOGS_NAME')
        try:
            _s3_client.put_object(Bucket=bucket_name,Body=item['body'],Key=item['key'])
        except Exception as e:
            raise


def get_logs_inventory():
    """ Generate List of logs from cloudwatch and put in S3 Bucket """
    try:
        
        
        logs_group_name = os.environ.get('LOG_GROUP_NAME')
        response = _logs.filter_log_events(logGroupName=f'{logs_group_name}')
        
        logs = response.get("events")
        for log in logs:
            log_stream = f"{log['logStreamName']}"
            log_name = f"{log['logStreamName']}".split('/')[-1]
            log_events = _logs.get_log_events(logGroupName=f'{logs_group_name}', logStreamName=f'{log_stream}').get('events')
            evnt_body =''
            for evnt in log_events:
               evnt_msg = f"{evnt['message']}"     
               evnt_body += evnt_msg 
            _bkt_put_item({
                'key':f'logs/{log_name}.log',
                'body':evnt_body
            })
        return "Logs files saved on S3 bucket" 
    except Exception as e:
        raise


def lambda_handler(event, context):
    global LOGGER
    LOGGER = logging.getLogger()
    LOGGER.setLevel(level=os.getenv('LOG_LEVEL', 'DEBUG').upper())
    LOGGER.info(f"received_event:{event}")

    resp = {
        "statusCode": 400,
        "body": json.dumps({"message": event})
    }

    try:
        logs_inventory = get_logs_inventory()
        resp["body"] = json.dumps({
            "message": logs_inventory
        })
        resp['statusCode'] = 200
    except Exception as e:
        resp["body"] = json.dumps({
            "message": f"ERROR:{str(e)}"
        })

    return resp