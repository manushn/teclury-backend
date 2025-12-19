import boto3
import os
from dotenv import load_dotenv

# LOAD ENV VARIABLES FIRST
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
TABLE_NAME = os.getenv("DYNAMO_TABLE")

if not AWS_REGION:
    raise RuntimeError("AWS_REGION is not set in .env")

if not TABLE_NAME:
    raise RuntimeError("DYNAMO_TABLE is not set in .env")

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

table = dynamodb.Table(TABLE_NAME)
