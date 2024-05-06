# import pandas as pd
# from langchain.chains import create_tagging_chain_pydantic
# from llm_applications.Derivati.preprocessing.functions import run_replace_string_function
# from llm_applications.Derivati.preprocessing.preprocessing_config import preprocessing_unicredit_dict, preprocessing_unicredit_cedola_dict
# from llm_applications.Derivati.setting.pydantic_schema import PydanticSchema_unicredit, PydanticSchema_unicredit_noLangChain


# def Unicredit_IssuerChain(input_kid, llm):

#     input_kid = run_replace_string_function(documents=input_kid, preprocessing_dict_static=preprocessing_unicredit_dict,
#                                             preprocessing_dict_regex=False,
#                                             preprocessing_dict_regex_dynamic=preprocessing_unicredit_cedola_dict)

#     base_chain = create_tagging_chain_pydantic(PydanticSchema_unicredit, llm)
#     base_guesses = base_chain.run(input_kid)
#     base_guesses_dict = dict(base_guesses)
#     df_guesses = pd.DataFrame.from_dict([base_guesses_dict])

#     return df_guesses


# def Unicredit_IssuerChain_noLangchain(input_kid, llm):

#     base_chain = create_tagging_chain_pydantic(PydanticSchema_unicredit_noLangChain, llm)
#     base_guesses = base_chain.run(input_kid)
#     base_guesses_dict = dict(base_guesses)
#     df_guesses = pd.DataFrame.from_dict([base_guesses_dict])

#     return df_guesses
