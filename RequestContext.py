import base64
import json
from decimal import Decimal
import os
BASE_ENCODED_KEY = 'isBase64Encoded'
BODY_KEY = 'body'


class RequestContext:
    
    def __init__(self, event):
        #print(event)
        # request_context = event['requestContext']
        # authorizer = request_context['authorizer']
        # if 'sessionContext' in authorizer:
        #     self.sessionContext = json.loads(base64.b64decode(authorizer['sessionContext']))
        # else:
            # self.sessionContext = {
            #     'accesskey': authorizer['accesskey'], 'secretkey': authorizer['secretkey'],
            #     'sessiontoken': authorizer['sessiontoken']
            # }
        
        # self.sessionContext = {
        #         'accesskey': 'xx',
        #         'secretkey': 'xxx'
        #     }
        # self.tenant = authorizer['tenant']
        # self.environment = self.sessionContext['environment'] if 'environment' in self.sessionContext else ''
        # self.roles = self.sessionContext.get('roles') if self.sessionContext.get('roles') is not None else []

        # Decode body of request
        self.payload = self.read_payload(event)

    def read_payload(self, event):
        payload = {}
        if BODY_KEY in event and event[BODY_KEY]:
            body = base64.b64decode(event[BODY_KEY]) if BASE_ENCODED_KEY in event and event[BASE_ENCODED_KEY] else event[
                BODY_KEY]
            payload = json.loads(body, parse_float=Decimal)
        return payload
    
