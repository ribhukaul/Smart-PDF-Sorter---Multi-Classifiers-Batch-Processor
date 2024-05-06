#!/usr/bin/env python
import json
import os
import shutil
from distutils.dir_util import copy_tree

from RequestContext import RequestContext
from ExtractionHandler import ExtractionHandler
from AWSInteraction.EnvVarSetter import EnvVarSetter

""" 
aws configure sso
For local testing needs to add the following environment variables to the config file
at AWSInteraction\config.json:
    - "S3_BUCKET": "dde-dev-working-671256662822-eu-south-1"
    - "SECRET_MANAGER_SUFFIX": "-llm-secret
    - "SECRET_MANAGER_PREFIX": "dde/dev/"
    - "REGION": "eu-south-1"
    - "AWS_PROFILE": "appicativo" (yoour profile name, to create your SSO profile follow 
    https://docs.aws.amazon.com/cli/latest/userguide/sso-configure-profile-token.html#sso-configure-profile-token-auto-sso)

For parallel execution:
https://aws.amazon.com/blogs/compute/parallel-processing-in-python-with-aws-lambda/
"""

# TODO: CODE TO ELIMINATE OLDER FILE FROM /TMP
def lambda_handler(event, context):
    # curretn dir
    # print()
    print("RICEVUTO RICHIESTA: ", event)
    request_context = RequestContext(event)
    env_setter = EnvVarSetter(request_context.payload)
    USE_LOCAL_KEYS = False # True if you want to use local keys
    env_setter.configure_lambda_env_vars(use_local_keys=USE_LOCAL_KEYS)


    # tesseract_path = os.path.join(os.getcwd(),'extractors/cv_extractor/tesseract')#]/tesseract.exe')
    # #
    # tmp_executable_path = os.path.join(os.environ['LOCAL_SAVE_FOLDER'],'tesseract')#'tesseract.exe')
    # #shutil.copyfile(tesseract_path, tmp_executable_path)
    # copy_tree(tesseract_path, tmp_executable_path)#+'.exe')
    # file_executable = os.path.join(tmp_executable_path, 'tesseract.exe')
    # os.chmod(file_executable, 0o755)
    # #shutil.copyfile(tmp_executable_path, tesseract_path)
    # os.environ['TESSERACT_CMD'] = file_executable
    # #os.environ['TESSERACT_CMD'] = tmp_executable_path




    try:
        extraction_handler = ExtractionHandler(request_context)
        extraction_handler.run()
        extracted_data = extraction_handler.extractions
        extracted_data_json = json.dumps(extracted_data)
        ## MOCKUP OUTPUT
        #     with open('mock_output.json', 'r') as f:
        #         extracted_data_json = f.read()

        return {
            'statusCode': 200,
            'extraction': extracted_data_json
        }
    except Exception as error:
            print(error)
            return {
                'statusCode': 404,
                'extraction': json.dumps({'error': repr(error)})
            }


# if __name__ == '__main__':
#    import os

#    import json

#    reqq = {
#    "TENANT": "waminsurance",
#                 "extractor_type": "complexity",
#                 "extraction_model": "extraction_model",
#                 "files": [
#                         {
#                                 "key": "waminsurance/workspaces/chris/UL22US_233_0723.pdf",
#                                 "type": "FILE"
#                         }
#                         # ,
#                         # {
#                         #         "key": "basepfts/workspaces/e/allianz (1).pdf",
#                         #         "type": "FILE"
#                         # }
#                 ]
#    }
#    reqq ={
#             "TENANT": "wamderivati", 
#             "extractor_type": "complexity", 
#             "extraction_model": "gpt-4", 
#             "files": [{
#                  "key": "wamderivati/workspaces/test derivati/allianz.pdf", 
#                  "type": "file"}]}
#    os.environ['ENV'] = 'local'
#    req = json.dumps(reqq)
#    event = {
#        "body": req}#"{\r\n  \"files\": [\"basepfts/workspaces/33/d" ], \"TENANT\": \"insurance\", \"extractor_type\": \"kid\"\r\n}"}
#    x = lambda_handler(event, None)
#    print(x)

    