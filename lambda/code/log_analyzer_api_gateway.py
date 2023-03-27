import boto3
import os
import csv
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # read LOG_FILE_PATH from environment variable
    log_file_path = os.getenv("LOG_FILE_PATH", None)
    if log_file_path is not None:
        bucket = log_file_path.split("/")[2]
        key = log_file_path.split("/", 3)[3]
        print("bucket: {}".format(bucket))
        print("key: {}".format(key))
        data = s3.get_object(Bucket=bucket, Key=key)['Body'].read().decode("utf-8")
        csvreader = csv.reader(data.splitlines())
        urls = {}
        selected_ip = ""
        eventBody = None
        eventJson = json.loads(json.dumps(event))
        if 'body' in eventJson.keys():
            eventBody = json.loads(eventJson['body'])
            if 'ip' in eventBody.keys():
                selected_ip = eventBody['ip']
        print("select urls for ip '{}':".format(selected_ip))
        count_tot = 0
        count_match = 0
        for row in csvreader:
            count_tot = count_tot + 1
            ip = row[0]
            if selected_ip is "" or selected_ip == ip:
                count_match = count_match + 1
                if row[2] in urls:
                    urls[row[2]] = urls[row[2]] + 1
                else:
                    urls[row[2]] = 1
        print("matches {} of {}".format(count_match, count_tot))
        return {"ip": selected_ip, "urls_count": urls}
    else:
        raise Exception("'LOG_FILE_PATH' environment variable not set!")