from openai import OpenAI
from utils import extract_code_from_response

def chat(prompt, function):
    """
    This function interacts with GPT through text.

    Args:
        prompt (str): Information provided by the user in this chat.
        model (str): The OpenAI model being used.
        messages (list): Context required for this chat.

    Returns:
        list: Information that includes the content of this chat.
    """
    client = OpenAI(api_key='sk-fnW7WGNc6sfkWrf1SZLiPdLPclvm38X4JcT1M9m4OXmfOQ4f', 
                    base_url='https://api.openai-proxy.org/v1')
    
    init_prompt = "I want to optimize the control structures of the decompiled code. Below are the optimization strategies I think should be adopted after analyzing the code, along with the function to be optimized. Please help me implement this optimization, and provide the optimized function at the end of your response."
    
    prompt = f"{init_prompt}\nOptimization:\n{prompt}\nCode:\n{function}"

    messages = []
    messages.append({"role":"user", "content":prompt})
    init_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
            )
    full_response = ''

    for chunk in init_response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
    messages.append({"role":"assistant", "content": full_response})

    optimized_code = extract_code_from_response(full_response)[-1]
    
    return optimized_code