  
import boto3
import os
import json

from botocore.exceptions import ClientError


class SecretManager(object):
    def __init__(self, endpoint_url, region_name):
        endpoint_url = endpoint_url
        region_name = region_name
        session = boto3.session.Session()
        self.client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
            endpoint_url=endpoint_url)

    def get_secret(self, secret_name):
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("The requested secret " + secret_name + " was not found")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                print("The request was invalid due to:", e)
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                print("The request had invalid params:", e)
            else:
                print(e)
            raise e
        else:
            # Decrypted secret using the associated KMS CMK
            # Depending on whether the secret was a string or binary,
            # one of these fields will be populated
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
        json_secret = json.loads(secret)
        return json_secret