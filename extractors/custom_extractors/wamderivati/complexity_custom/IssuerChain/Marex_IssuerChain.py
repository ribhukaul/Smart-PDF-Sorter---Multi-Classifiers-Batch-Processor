# import pandas as pd
# from langchain.chains import create_tagging_chain_pydantic
# from llm_applications.Derivati.preprocessing.functions import run_replace_string_function
# from llm_applications.Derivati.preprocessing.preprocessing_config import preprocessing_marex_dict, preprocessing_marex_cedola_dict
# from llm_applications.Derivati.setting.pydantic_schema import PydanticSchema_preprocess_marex, PydanticSchema


# def Marex_IssuerChain(input_kid, llm):

#     input_kid = run_replace_string_function(documents=input_kid, preprocessing_dict_static=preprocessing_marex_dict, preprocessing_dict_regex=preprocessing_marex_cedola_dict, preprocessing_dict_regex_dynamic=False)

#     base_chain = create_tagging_chain_pydantic(PydanticSchema_preprocess_marex, llm)
#     base_guesses = base_chain.run(input_kid)
#     base_guesses_dict = dict(base_guesses)
#     df_guesses = pd.DataFrame.from_dict([base_guesses_dict])

#     return df_guesses





