from io import StringIO
import os
import boto3
import pandas as pd
import math
from dotenv import load_dotenv

load_dotenv()

def copy_file_from_s3(s3_file_key, local_directory):
  try:
    # Create an S3 client
    s3 = boto3.client('s3')

    bucket_name = os.environ["BUCKET_NAME"]

    # Ensure the local directory exists
    os.makedirs(local_directory, exist_ok=True)

    # Create the local file path
    local_file_path = os.path.join(local_directory, os.path.basename(s3_file_key))

    # Download the file from S3 to the local file path
    s3.download_file(bucket_name, s3_file_key, local_file_path)
  except Exception as e:
    print("ERROR: Could not retrieve MIMIC-III Dataset from s3. Have you added the environment variables from .env.sample into .env?")
    print(e)

def readS3CSV(file_key):
  try:
    s3 = boto3.client('s3')
    bucket_name = os.environ['BUCKET_NAME']
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    return pd.read_csv(obj['Body'])
  except Exception as e:
    print("ERROR: Could not retrieve MIMIC-III Dataset from s3. Have you added the environment variables from .env.sample into .env?")
    print(e)

def readS3PartialCSV(file_key, number_of_lines=10, offset=0):
  """
  Reads only part of the specified CSV.

  Parameters:
  file_key (string): The name of the file.
  number_of_lines (int): The number of lines to retrieve; includes headers.

  Returns:
  pandas.DataFrame: The sum of the two numbers.
  """
  try:
    s3 = boto3.client('s3')
    bucket_name = os.environ['BUCKET_NAME']

    # Define the SQL query to read the first 10 lines
    sql_query = f"SELECT * FROM S3Object LIMIT {number_of_lines}"

    # Configure the S3 Select request
    select_params = {
        'Bucket': bucket_name,
        'Key': file_key,
        'ExpressionType': 'SQL',
        'Expression': sql_query,
        'InputSerialization': {
            'CSV': {
                'FileHeaderInfo': 'NONE',  # Print the full output
            },
            'CompressionType': 'NONE'
        },
        'OutputSerialization': {
            'CSV': {}
        }
    }

    # Execute the S3 Select query
    response = s3.select_object_content(**select_params)

    csv_data = ''
    # Process the response and print the first 10 lines
    for event in response['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            csv_data += records

    csv_file = StringIO(csv_data)
    return pd.read_csv(csv_file)
  except Exception as e:
    print("ERROR: Could not retrieve MIMIC-III Dataset from s3. Have you added the environment variables from .env.sample into .env?")
    print(e)

def timedelta_to_interval(time_diffs):
    interval_strings = []
    
    for td in time_diffs:
        months = td.days / 30.0  # Convert timedelta to approximate number of months

        if 0 < months <= 1:
            interval = '0-1m'
        elif 1 < months <= 3:
            interval = '1-3m'
        elif 3 < months <= 6:
            interval = '3-6m'
        elif 6 < months <= 12:
            interval = '6-12m'
        else:
            interval = '12+m'
        
        interval_strings.append(interval)
    
    return interval_strings