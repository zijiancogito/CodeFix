import os
from openai import OpenAI

import subprocess
import re


def compile(code, d, candicate_id=0):
    sub_d = os.path.join(d, str(candicate_id))
    if not os.path.exists(sub_d):
        os.mkdir(sub_d)
    c_file = f'{sub_d}/source.c'
    with open(c_file, 'w') as f:
        f.write(code)

    o_file = f'{sub_d}/binary.out'
    compile_command = ["gcc", c_file, "-o", o_file]
    
    try:
        result = subprocess.run(compile_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return parse_gcc_errors(e.stderr.decode())

    return []

def parse_gcc_errors(error_message):
    error_pattern = r'(.+\.c):(\d+):\d+: (error|warning): (.+)'
    errors = re.findall(error_pattern, error_message)

    parsed_errors = []
    for error in errors:
        file, line, error_type, message = error
        parsed_errors.append({"file": file, "line": line, "type": error_type, "message": message})

    return parsed_errors

def build_error_prompt(errors):
    init_prompt = "This is the error message from compiler:"
    err_prompt = []
    for err in errors:
        if err['type'] == 'warning':
            continue
        line = err['line']
        msg = err['message']
        err_prompt.append(f"Line {line}: {msg}")

    if len(err_prompt) == 0:
        return ""
    err_prompt = '\n'.join(err_prompt)
    prompt = f"{init_prompt}\n{err_prompt}"
    return prompt

def chat(code, d):
    messages = []
    head_prompt = "Please fix this code to be recompilable:"
    tail_prompt = "Please only output the fixed code."

    candicate_id = 0

    errors = compile(code, d, candicate_id)
    err_prompt = build_error_prompt(errors)
    if len(err_prompt) == 0:
        return code

    client = OpenAI(api_key='sk-fnW7WGNc6sfkWrf1SZLiPdLPclvm38X4JcT1M9m4OXmfOQ4f', 
                    base_url='https://api.openai-proxy.org/v1')
    while True:
        prompt = f"{head_prompt}:\n{code}\n{err_prompt}\n{tail_prompt}"
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
                # print(chunk.choices[0].delta.content, end="")
        # print()
        messages.append({"role":"assistant", "content": full_response})
        code = '\n'.join(full_response.split('\n')[1:-1])
        errors = compile(code, d, candicate_id)
        candicate_id += 1
        err_prompt = build_error_prompt(errors)

        if len(err_prompt) == 0:
            return code
        if candicate_id == 20:
            return None


if __name__ == '__main__':
    # code = None
    # work_space = '../test/'
    # with open('../test/dec.c', 'r') as f:
        # code = f.read().strip()
    # fixed_code = chat(code, work_space)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='path to chall dir')

    args = parser.parse_args()

    code = None
    with open(os.path.join(args.dir, 'starter.c'), 'r') as f:
        code = f.read()

    fixed_code = chat(code, args.dir)

    with open(os.path.join(args.dir, 'final.c'), 'w') as f:
        f.write(fixed_code)

