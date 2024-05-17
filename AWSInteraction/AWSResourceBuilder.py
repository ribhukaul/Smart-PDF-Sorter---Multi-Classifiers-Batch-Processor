import boto3
import os

class AWSResourceBuilder():
    
    def __init__(self) -> None:
        self.session = self._create_session()
        

    def _create_session(self):
        if os.getenv('ENV') == 'local':
            self.profile = os.environ['AWS_PROFILE']
            self.region = os.environ['REGION']
            return boto3.Session(profile_name=self.profile, region_name=self.region)
        else:
            return boto3.Session()
    
    def get_s3_client(self):
        return self.session.client('s3')
    
    def get_secret_manager_client(self):
        return self.session.client(service_name='secretsmanager')

    