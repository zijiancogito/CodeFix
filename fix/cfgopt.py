import os
from openai import OpenAI

import subprocess
import re

def build_review_prompt(review, review_tp):
    if review_tp == 'condition combination':
        return f"The control statements or conditions in the specified lines of the code ({review}) show overlapping and redundant judgments. Please appropriately merge or reorganize them to simplify the logic."
    
    return None

def chat(code, review, review_tp):
    messages = []

    head_prompt = "This is a piece of code output by the Hex-Rays. Please make modifications to the code according to my requirements, keeping the original variable names and other elements in the code as much as possible. Changes should be made only to the control structures and the order of statements."
    mid_prompt = "Here are my suggested modifications:"
    tail_prompt = "Please only output the fixed code."

    review_prompt = build_review_prompt(review, review_tp)

    if review_prompt == None:
        return code

    client = OpenAI(api_key='sk-fnW7WGNc6sfkWrf1SZLiPdLPclvm38X4JcT1M9m4OXmfOQ4f',
                    base_url='https://api.openai-proxy.org/v1')

    prompt = f"{head_prompt}:\n{code}\n{mid_prompt}:\n{review_prompt}\n{tail_prompt}"
    messages.append({"role":"user", "content":prompt})
    response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            stream=True,
    )
    full_response = ''

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content

    print(full_response)

if __name__ == '__main__':
    code = None
    work_space = '../test/dec.c'
    with open(work_space, 'r') as f:
        code = f.read()

    review = 'Line 6, 7'
    review_tp = 'condition combination'
    chat(code, review, review_tp)

