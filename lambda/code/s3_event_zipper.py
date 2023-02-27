import boto3
import zipfile
from io import BytesIO
import os

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # read default output prefix from environment variable
    output_folder = os.getenv("OUTPUT_PREFIX", "default_output")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN", None)
    # process only if we can find bucket name and file on event
    if "Records" in event and len(event["Records"][0]) > 0 and"s3" in event["Records"][0]:
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file = event["Records"][0]["s3"]["object"]["key"]
        if file is not None and file.endswith(".zip"):
            # unzip file, and push each file to output folder subfolder
            simple_file_name = file.split("/")[-1].split(".")[0]
            zip_obj = s3.get_object(Bucket=bucket_name, Key=file)
            buffer = BytesIO(zip_obj["Body"].read())
            with zipfile.ZipFile(buffer, 'r') as zip_ref:
                for filename in zip_ref.namelist():
                    content = zip_ref.open(filename)
                    s3.put_object(Bucket=bucket_name, Key=output_folder + "/" + simple_file_name + "/" + filename, Body=content)
            if sns_topic_arn is not None:
                sns.publish(TopicArn=sns_topic_arn, Subject="Extraction successful", Message="file '{}' extracted successfully to '{}'".format(file, (output_folder + "/" + simple_file_name + "/")))
        else:
            # zip the file, abd put into output folder
            archive = BytesIO()
            zipped_file_name = file.split("/")[-1]
            archive_name = zipped_file_name.split(".")[0]

            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
                with zip_archive.open(zipped_file_name, 'w') as file1:
                    data = s3.get_object(Bucket=bucket_name, Key=file)
                    file1.write(data['Body'].read())
            archive.seek(0)
            s3.put_object(Bucket=bucket_name, Key=output_folder + "/" + archive_name + ".zip", Body=archive)
            if sns_topic_arn is not None:
                sns.publish(TopicArn=sns_topic_arn, Subject="Compression successful", Message="file '{}' compressed successfully to '{}'".format(file, (output_folder + "/" + archive_name + ".zip")))
    else:
        raise Exception("Lambda not triggered by S3 event")
        