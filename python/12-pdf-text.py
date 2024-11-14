import boto3 
import os
from dotenv import load_dotenv
 
load_dotenv()

os.environ['AWS_DEFAULT_REGION'] = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
os.environ['AWS_ACCESS_KEY_ID'] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv("AWS_SECRET_ACCESS_KEY")
import time


def start_job(client, s3_bucket_name, object_name):
    response = None
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3_bucket_name,
                'Name': object_name
            }})

    return response["JobId"]


def is_job_complete(client, job_id):
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(1)
        response = client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status


def get_job_results(client, job_id):
    pages = []
    time.sleep(1)
    response = client.get_document_text_detection(JobId=job_id)
    pages.append(response)
    print("Resultset page received: {}".format(len(pages)))
    next_token = None
    if 'NextToken' in response:
        next_token = response['NextToken']

    while next_token:
        time.sleep(1)
        response = client.\
            get_document_text_detection(JobId=job_id, NextToken=next_token)
        pages.append(response)
        print("Resultset page received: {}".format(len(pages)))
        next_token = None
        if 'NextToken' in response:
            next_token = response['NextToken']

    return pages


if __name__ == "__main__":
    # Document
    s3_bucket_name = "ki-textract-demo-docs"
    document_name = "Amazon-Textract-Pdf.pdf"
    region = "us-east-1"
    client = boto3.client('textract', region_name=region)

    job_id = start_job(client, s3_bucket_name, document_name)
    print("Started job with id: {}".format(job_id))
    if is_job_complete(client, job_id):
        response = get_job_results(client, job_id)

    # print(response)

    # Print detected text
    for result_page in response:
        for item in result_page["Blocks"]:
            if item["BlockType"] == "LINE":
                print('\033[94m' + item["Text"] + '\033[0m')


'''
Started job with id: d91d44d54f7676f532fd81b18e50e59ece5053bf40e99947df4c2bd9243c3708
Job status: IN_PROGRESS
Job status: IN_PROGRESS
Job status: IN_PROGRESS
Job status: SUCCEEDED
Resultset page received: 1
Amazon Textract
Amazon Textract is a s

'''