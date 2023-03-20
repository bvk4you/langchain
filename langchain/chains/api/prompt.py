# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

# API_URL_PROMPT_TEMPLATE = """You are given the below API Documentation:
# {api_docs}
# Using this documentation, generate the full API url to call for answering the user question.
# You should build the API url in order to get a response that is as short as possible, while still getting the necessary information to answer the question. Pay attention to deliberately exclude any unnecessary pieces of data in the API call.

# Question:{question}
# API url:"""
API_URL_PROMPT_TEMPLATE = """""
Given a user question and an API documentation text, extract the appropriate API information including the HTTP method, URL, parameters, and request body. Return the results as a JSON dictionary string. Here is the user question:

"{question}"

And here is the API documentation text:

"{api_docs}"

Please identify the relevant API, method, URL make sure to add the required query parameters to the URL itself, parameters, and body (include only user added fields) for this question, and return the information as a JSON dictionary string.Use the following
keys as it is API, Method, URL, Body and also include all the parameters and their values to the final URL
Avoid any extra notes apart from the json dictionary

"""
API_URL_PROMPT = PromptTemplate(
    input_variables=[
        "api_docs",
        "question",
    ],
    template=API_URL_PROMPT_TEMPLATE,
)

API_RESPONSE_PROMPT_TEMPLATE = (
    API_URL_PROMPT_TEMPLATE
    + """ {api_url}

Here is the response from the API:

{api_response}

return the response as it is as the result
Result:"""
)

API_RESPONSE_PROMPT = PromptTemplate(
    input_variables=["api_docs", "question", "api_url", "api_response"],
    template=API_RESPONSE_PROMPT_TEMPLATE,
)
