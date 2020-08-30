# https://aws.amazon.com/developers/getting-started/python
# After setting up the AWS Secrets Manager with:
# 1) Secret name : git-token
# 2) key-value:  oauthToken and gitHubToken
#
# you can use the following Python code to retrieve the secrets

import sys
import boto3
import base64
import json
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "git-token"
    region_name = "us-west-1"

    # Create Secrets Manager client first
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
    except:
        ex = sys.exc_info()[0]
        err_msg = "Error: failed to retrieve %s secret (%s)." % (secret_name, ex)
        print(err_msg)
        sys.exit(1)      
    else:
        # Decrypt secret based on string or binary
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])

        return json.loads(secret)    
            
secret = get_secret()

### print all secrets
for key, value in secret.items():
    print(key, ' : ', value)

### or if you know the secret key and need the value
print('oauthToken secret = '+secret['oauthToken'])