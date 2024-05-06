import json
import os
import traceback
import uuid

from AWSInteraction.AWSResourceBuilder import AWSResourceBuilder

BODY_KEY = 'body'
STATUS_CODE_KEY = 'statusCode'


class S3ExtractionHandler:


    def __init__(self, file_key, bucket=None) -> None:
        self.__set_download_folder()
        self.file_key = file_key
        if bucket is None:
            self.bucket = os.getenv('S3_BUCKET')
        else:
            self.bucket = bucket
        builder = AWSResourceBuilder()
        self.s3 = builder.get_s3_client()
    
    def __set_download_folder(self):
        if os.getenv('ENV') == 'local':
            self.download_folder = 'tmp'
        else:
            self.download_folder = '/tmp'
    
    def read(self):
        s3_object = self.s3.Object(
            bucket_name=self.bucket,
            key=self.file_key)
        try:
            return {STATUS_CODE_KEY: 200, BODY_KEY: s3_object.get()['Body'].read()}#.decode('UTF-8')}
        except Exception as error:
            print(error)
            traceback.print_exc()
            return {STATUS_CODE_KEY: 404, BODY_KEY: json.dumps({'message': 'file not found'})}
    
    def download(self, file_key, download_path=""):
        if download_path == "":
            # get file extension
            extension = file_key.split('.')[-1]
            file_name = str(uuid.uuid4()) + '.' + extension
            download_path = os.path.join(self.download_folder, file_name)
        try:
            self.s3.download_file(self.bucket, file_key, download_path)
            return {STATUS_CODE_KEY: 200, BODY_KEY: download_path}
        except Exception as error:
            print(error)
            traceback.print_exc()
            return {STATUS_CODE_KEY: 404, BODY_KEY: json.dumps({'message': 'file not found'})}

    def list_files(self, prefix=''):
        try:
            key=self.file_key
            if prefix != '':
                key = prefix
                
            response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=key)
            # create a lis tof all the files in the folder (excluding the subfolders)
            f_k_list = [f_k["Key"] for f_k in response['Contents'] if os.path.dirname(f_k["Key"]) == key]

            return {STATUS_CODE_KEY: 200, BODY_KEY: f_k_list}
        except Exception as error:
            print(error)
            traceback.print_exc()
            return {STATUS_CODE_KEY: 404, BODY_KEY: json.dumps({'message': 'file not found'})}
