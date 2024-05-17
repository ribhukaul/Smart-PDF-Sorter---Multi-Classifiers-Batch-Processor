import os
import json

from AWSInteraction.AWSSecretsHandler import SecretsManagerExtractionHandler
"""
In order to run the code locally while trying to connect to the S3 bucket and 
AWS Secrets Manager, you need to configure a local auth profile on
    https://docs.aws.amazon.com/cli/latest/userguide/sso-configure-profile-token.html#sso-configure-profile-token-auto-sso)
and activate the and set the variable 
AWS_PROFILE in AWSInteraction//config.json to the name of the profile you created.
"""


class EnvVarSetter():


    def __init__(self, payload=None, tenant=None) -> None:

        with open('AWSInteraction//config.json') as json_file:
            self.config = json.load(json_file)

        if os.environ.get("ENV") == None:
            os.environ["ENV"] = "local"

        if os.getenv('ENV') == 'local':
            os.environ['LOCAL_SAVE_FOLDER'] = 'tmp'
        else:
            os.environ['LOCAL_SAVE_FOLDER']  = '/tmp'

        self.tenant = tenant
        if payload is not None:
            self.payload = payload
            self.tenant = payload['TENANT']

    # LAMBDA
    def configure_lambda_env_vars(self, use_local_keys=False) -> None:
        """
        Set the environment variables for the lambda function.
        use_local_keys: if True, the API keys are taken from the local config file.
        """
        if os.environ["ENV"] == "local":
            self._set_env_variables("aws_configs")
        self.set_locally_saved_env_vars()
        self.set_aws_secret_manager_env_vars()

        if use_local_keys and os.environ["ENV"] == "local":
            self._set_env_variables("local")
            self._set_env_variables("api_keys")

    # LOCAL RUN (need api keys in config.json)
    def configure_local_env_vars(self) -> None:
        """
        Set the environment variables for local testing.
        For this set up the config file should be modified by adding API keys.
        """
        self.set_locally_saved_env_vars()
        self._set_env_variables("local")
        self._set_env_variables("api_keys")


    def set_locally_saved_env_vars(self) -> None:
        """
        Set the environment variables that are saved locally in the config file.
        """
        # set tenant vars
        self._set_env_variables("general")
        self._set_env_variables(self.tenant)

    def set_aws_secret_manager_env_vars(self) -> None:
        """
        Set the environment variables that are saved in AWS Secrets Manager.
        """

        sm_handler = SecretsManagerExtractionHandler()

        # Create secret name
        secret_suffix = os.environ["SECRET_MANAGER_SUFFIX"]
        secret_prefix = os.environ["SECRET_MANAGER_PREFIX"]
        secret_name = f"{secret_prefix}{self.tenant}{secret_suffix}"

        # Get secret
        secret = sm_handler.get_secret_value(secret_name, as_dict=True)

        # set the API keys
        for key, value in secret.items():
            os.environ[key] = value

    def _set_env_variables(self, variable_group) -> None:
        """
        Set the environment variables from a dictionary.
        """
        env_variables = self.config.get(variable_group)
        if env_variables is not None:
            for key, value in env_variables.items():
                os.environ[key] = value
        else:
            print(f"Variable group {variable_group} not found in the config file.")

