from io import StringIO
import os
import boto3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def readS3CSV(file_key):
  try:
    s3 = boto3.client('s3')
    bucket_name = os.environ['BUCKET_NAME']

    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    return pd.read_csv(obj['Body'])
  except:
    print("ERROR: Could not retrieve MIMIC-III Dataset from s3. Have you added the environment variables from .env.sample into .env?")