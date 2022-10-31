# -*- coding: utf-8 -*-

import boto3
import json
import logging
import os

_s3_client = boto3.client('s3')
_ddb = boto3.resource('dynamodb')


def _ddb_put_item(item):
    """ Insert Item into DynamoDb Table """
    if os.environ.get('DDB_TABLE_NAME'):
        _ddb_table = _ddb.Table(os.environ.get('DDB_TABLE_NAME'))
        try:
            _ddb_table.put_item(Item=item)
        except Exception as e:
            raise


def get_bkts_inventory():
    """ Generate List of logs in S3 Buckets """
    try:
        
        bucket_name = os.environ.get('BUCKET_LOGS_NAME')
        response = _s3_client.list_objects_v2(Bucket=bucket_name, Prefix = "logs/")
        
        files = response.get("Contents")
        files_filtered = filter(lambda file: file['Key'].endswith(".log"), files)
        for file in files_filtered:
            file_name = f"{file['Key']}"
            file_content = _s3_client.get_object(Bucket=f"{bucket_name}" , Key=f"{file['Key']}")['Body'].read().decode('utf-8')
            _ddb_put_item({"file_name":file_name,"file_content":file_content})
             
        return "Logs exported to DynamoDB" 
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
        bkt_inventory = get_bkts_inventory()
        resp["body"] = json.dumps({
            "message": bkt_inventory
        })
        resp['statusCode'] = 200
    except Exception as e:
        resp["body"] = json.dumps({
            "message": f"ERROR:{str(e)}"
        })

    return resp