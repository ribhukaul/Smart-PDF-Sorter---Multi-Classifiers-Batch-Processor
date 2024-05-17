# AZURE OPENAI COSTS
# https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/


cost_per_token = {
    "input": {
        "gpt-4-turbo": 0.00001,
        "gpt-4": 0.000028,
        "gpt-3.5-turbo-16k": 0.0000005,
        "gpt-3.5-turbo": 0.0000014,
    },
    "output": {
        "gpt-4-turbo": 0.000028,
        "gpt-4": 0.000056,
        "gpt-3.5-turbo-16k": 0.0000014,
        "gpt-3.5-turbo": 0.0000019,
    },
    "azure": 0.016,
}
available_costs = [
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo",
    "azure",
]
