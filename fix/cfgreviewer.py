import os
import subprocess
import re

from openai import OpenAI


def chat(code):
    messages = []

    # head_prompt = "Please check the control structure in this code for redundancy in control logic or conditional judgments. Answer with 'yes' or 'no' and list each overlap you identify."
    # head_prompt = "Please check the control structures in this code to see if there is any redundancy in the control logic or the conditions for control judgment. Answer with 'yes' or 'no' only and list the line number range of the redundant code."
    # head_prompt = "Please check the control structures in this code snippet for potentially redundant control conditions and statements. Only answer 'yes' or 'no', and list the line number ranges of any redundant parts of the code."
    head_prompt = "Please check the control structures in this code segment. Are there any control conditions and statements that can be combined? Answer yes or no, and list the line numbers of the code that can be combined."
    tail_prompt = """
        Respond in the following format:
        Yes/No
        Line x, y, ...
        """
    
    candicate_id = 0
    client = OpenAI(api_key='sk-fnW7WGNc6sfkWrf1SZLiPdLPclvm38X4JcT1M9m4OXmfOQ4f',
                    base_url='https://api.openai-proxy.org/v1')

    prompt = f"{head_prompt}:\n{code}\n{tail_prompt}"
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

    if 'No' in full_response:
        return None

    return full_response.split('\n')[1:]


if __name__ == '__main__':
    code = None
    work_space = '../test/dec.c'
    with open(work_space, 'r') as f:
        code = f.read()

    chat(code)

