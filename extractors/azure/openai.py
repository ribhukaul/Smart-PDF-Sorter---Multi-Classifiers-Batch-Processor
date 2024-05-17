from langchain_openai import AzureChatOpenAI
import os


def azure_openai_model(model="gpt-4-turbo", temperature=0, verbose=True):
    """Create an AzureChatOpenAI object.

    Args:
        model (str, optional): model name. Defaults to 'gpt-3.5'.
        temperature (int, optional): temerature for the model. Defaults to 0.
        verbose (bool, optional): varbosity of the model object. Defaults to True.

    Raises:
        ValueError: if the model is not supported.

    Returns:
        AzureChatOpenAI: azure chat open ai model form langchain.
    """

    if model == "gpt-3.5-turbo":
        DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_GPT35_DEP_NAME")
    elif model == "gpt-3.5-turbo-16k":
        DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_GPT35_16K_DEP_NAME")
    elif model == "gpt-4":
        DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_GPT4_DEP_NAME")
    elif model == "gpt-4-turbo":
        DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_GPT4_TURBO_DEP_NAME")

    else:
        raise ValueError("Model not supported")

    az_model = AzureChatOpenAI(
        deployment_name=DEPLOYMENT_NAME,
        verbose=verbose,
        temperature=temperature,
        openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    )

    return az_model

