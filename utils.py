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
  except Exception as e:
    print("ERROR: Could not retrieve MIMIC-III Dataset from s3. Have you added the environment variables from .env.sample into .env?")
    print(e)

def readS3PartialCSV(file_key, number_of_lines=10):
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