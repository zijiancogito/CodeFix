import re
import os

def extract_code_from_response(response):
    print(response)
    import pdb
    pdb.set_trace()
    pattern = r'```c\n(.*?)```'
    matches = re.findall(pattern, response, re.DOTALL)
    return matches[-1]
