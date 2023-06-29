import os
import openai
import yaml
from yaml.loader import SafeLoader

key = yaml.load(open('Llm_Config.yml'),Loader=SafeLoader)
openai.api_key = key['openai_api_key']

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]