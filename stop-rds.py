import json
import boto3
import botocore
from botocore.exceptions import ClientError

rds = boto3.client('rds')

def lambda_handler(event, context):
    try:
        print('Grabbing DB instances')
        dbs = rds.describe_db_instances()
        for db in dbs['DBInstances']:
            rdsname = db['DBInstanceIdentifier']
            arn = db['DBInstanceArn']
            tags = rds.list_tags_for_resource(ResourceName=arn)['TagList']
            for tag in tags:
                if tag['Key'] == 'StayOffline':
                    print('Tagged instance found: ' + rdsname)
                    print('Stopping instance.')
                    try:
                        rds.stop_db_instance(DBInstanceIdentifier=rdsname)
                    except:
                        print('Database already offline.')
    except ClientError as error:
        print(error)
    return
    {
        'message' : "Execution complete"
    }