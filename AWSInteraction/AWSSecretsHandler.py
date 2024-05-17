import json
from AWSInteraction.AWSResourceBuilder import AWSResourceBuilder


class SecretsManagerExtractionHandler:

    def __init__(self) -> None:
        builder = AWSResourceBuilder()
        self.sm = builder.get_secret_manager_client()

    
    def get_secret(self, secret_name):
        """ Get the secret from AWS Secrets Manager.

        secret_name: The name of the secret to retrieve.

        Returns the secret string with the follwoing format:
            
            'ARN': 'string',
            'Name': 'string',
            'VersionId': 'string',
            'SecretBinary': b'bytes',
            'SecretString': 'string',
            'VersionStages': [
                'string',
            ],
            'CreatedDate': datetime(2015, 1, 1)
        }
        """  

        secret = self.sm.get_secret_value(SecretId=secret_name)
       
        return secret
    
    def get_secret_value(self, secret_name, as_dict=False):
        """ Get the secret from AWS Secrets Manager.

        secret_name: The name of the secret to retrieve.
        as_dict: If True, the secret is returned as a dictionary, otherwise as a string.

        Returns the secret string.
        """  

        secret = self.get_secret(secret_name)
        secret_value = secret['SecretString']
        if as_dict:
            secret_value = json.loads(secret_value)

        return secret_value

    