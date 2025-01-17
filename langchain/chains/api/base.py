"""Chain that makes API calls and summarizes the responses to answer a question."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, root_validator

from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

from langchain.chains.api.prompt import API_RESPONSE_PROMPT, API_URL_PROMPT
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain
from langchain.llms.base import BaseLLM
from langchain.prompts import BasePromptTemplate
from langchain.requests import RequestsWrapper
import json
import re
import random
import string


class APIChain(Chain, BaseModel):
    """Chain that makes API calls and summarizes the responses to answer a question."""

    api_request_chain: LLMChain
    api_answer_chain: LLMChain
    requests_wrapper: RequestsWrapper = Field(exclude=True)
    api_docs: str
    question_key: str = "question"  #: :meta private:
    output_key: str = "output"  #: :meta private:

    @property
    def input_keys(self) -> List[str]:
        """Expect input key.

        :meta private:
        """
        return [self.question_key]

    @property
    def output_keys(self) -> List[str]:
        """Expect output key.

        :meta private:
        """
        return [self.output_key]

    @root_validator(pre=True)
    def validate_api_request_prompt(cls, values: Dict) -> Dict:
        """Check that api request prompt expects the right variables."""
        input_vars = values["api_request_chain"].prompt.input_variables
        expected_vars = {"question", "api_docs"}
        if set(input_vars) != expected_vars:
            raise ValueError(
                f"Input variables should be {expected_vars}, got {input_vars}"
            )
        return values

    @root_validator(pre=True)
    def validate_api_answer_prompt(cls, values: Dict) -> Dict:
        """Check that api answer prompt expects the right variables."""
        input_vars = values["api_answer_chain"].prompt.input_variables
        expected_vars = {"question", "api_docs", "api_url", "api_response"}
        if set(input_vars) != expected_vars:
            raise ValueError(
                f"Input variables should be {expected_vars}, got {input_vars}"
            )
        return values
    
    def generate_random_string(self,length):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def is_sensitive_word(self,word):
        # for keyword in sensitive_keywords:
        #     if keyword.lower() in word.lower():
        #         return True
        # Check if the word contains both alphabetical and numerical characters
        if re.search(r'[a-zA-Z]', word) and re.search(r'\d', word):
            return True
        return False
    
    def remove_empty_query_params(self,url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        cleaned_query_params = {key: value for key, value in query_params.items() if value[0]}

        cleaned_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                urlencode(cleaned_query_params, doseq=True),
                parsed_url.fragment,
            )
        )

        return cleaned_url
    
    def process_string(self,input_string):
        # Tokenize the input_string
        words = re.findall(r'\b\w+\b', input_string)
        print(input_string)
       # Identify sensitive words and create a mapping to dummy words
        word_mapping = {}
        for word in words:
            if self.is_sensitive_word(word):
                dummy_word =self. generate_random_string(5)
                while dummy_word in word_mapping:  # Ensure unique dummy words
                    dummy_word = self.generate_random_string(5)
                word_mapping[dummy_word] = word

        print(word_mapping)
    # Replace sensitive words with dummy words
        modified_string = input_string
        for dummy_word, real_word in word_mapping.items():
            modified_string = modified_string.replace(real_word, dummy_word)

        print('modified string',modified_string)

        # Send the modified string to the API and get the response
        response = self.api_request_chain.predict(
            question=modified_string, api_docs=self.api_docs
        )
        print('original api response',response)
        response = response.replace('Answer: ', '', 1)

        # Replace dummy words with the real words in the response
        for dummy_word, real_word in word_mapping.items():
            response = response.replace(dummy_word, real_word)
        
        print('Modified api response',response)

        return response
    
    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        question = inputs[self.question_key]
        
        api_url = self.process_string(question)

        self.callback_manager.on_text(
            api_url, color="green", end="\n", verbose=self.verbose
             )
        
        baseurl = "https://bpa-adhoc4.cisco.com/bpa/api/v1.0/"

        api_urlData = json.loads(api_url)
        if(api_urlData["Method"]=='GET'):  
            api_response = self.requests_wrapper.get(baseurl+self.remove_empty_query_params(api_urlData['URL']))
            self.callback_manager.on_text(
            api_response, color="yellow", end="\n", verbose=self.verbose
            )
        elif(api_urlData["Method"]=='PUT'):
            api_response = self.requests_wrapper.put(
                self.remove_empty_query_params(api_urlData['URL']),api_urlData['Body'])
            self.callback_manager.on_text(
            api_response, color="yellow", end="\n", verbose=self.verbose
            )
        #answer = self.api_answer_chain.predict(
         #   question=question,
          #  api_docs=self.api_docs,
           # api_url=api_url,
            #api_response=api_response,
        #)
        return {self.output_key: api_response}

    @classmethod
    def from_llm_and_api_docs(
        cls,
        llm: BaseLLM,
        api_docs: str,
        headers: Optional[dict] = None,
        api_url_prompt: BasePromptTemplate = API_URL_PROMPT,
        api_response_prompt: BasePromptTemplate = API_RESPONSE_PROMPT,
        **kwargs: Any,
    ) -> APIChain:
        """Load chain from just an LLM and the api docs."""
        get_request_chain = LLMChain(llm=llm, prompt=api_url_prompt)
        requests_wrapper = RequestsWrapper(headers=headers)
        get_answer_chain = LLMChain(llm=llm, prompt=api_response_prompt)
        return cls(
            api_request_chain=get_request_chain,
            api_answer_chain=get_answer_chain,
            requests_wrapper=requests_wrapper,
            api_docs=api_docs,
            **kwargs,
        )

    @property
    def _chain_type(self) -> str:
        return "api_chain"
