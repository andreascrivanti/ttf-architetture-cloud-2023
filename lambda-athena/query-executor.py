import boto3
import time

def lambda_handler(event, context):
    client = boto3.client('athena')
    output='s3://ascrivanti-data-analysis/output'
    response = client.start_query_execution(
        QueryString='SELECT * FROM weblog',
        QueryExecutionContext={
            'Database': 'ttf'
        },
        ResultConfiguration={
            'OutputLocation': output
        }
    )
    queryId = response["QueryExecutionId"]
    status = client.get_query_execution(
        QueryExecutionId=queryId
    )
    st = status["QueryExecution"]["Status"]["State"]
    while st == 'QUEUED' or st == 'RUNNING':
        time.sleep(1)
        status = client.get_query_execution(
            QueryExecutionId=queryId
        )
        st = status["QueryExecution"]["Status"]["State"]
    res = client.get_query_results(QueryExecutionId=queryId, MaxResults=2)
    return res