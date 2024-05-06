# import pandas as pd
# from langchain.chains import create_tagging_chain_pydantic
# # from Derivati.preprocessing.functions import run_replace_string_function
# # from Derivati.setting.pydantic_schema import PydanticSchema_akros, PydanticSchema


# def Akros_IssuerChain(input_kid, llm):

#     input_kid = run_replace_string_function(documents=input_kid, preprocessing_dict_static=False, preprocessing_dict_regex=False, preprocessing_dict_regex_dynamic=False)

#     base_chain = create_tagging_chain_pydantic(PydanticSchema_akros, llm)
#     base_guesses = base_chain.run(input_kid)
#     base_guesses_dict = dict(base_guesses)
#     df_guesses = pd.DataFrame.from_dict([base_guesses_dict])

#     return df_guesses





