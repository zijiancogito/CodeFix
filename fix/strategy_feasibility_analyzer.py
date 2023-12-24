from openai import OpenAI

# When using API calls to GPT, context needs to be passed through the "message".
# You can change the context of GPT by adjusting the content of the "message".

# In the initial call, GPT will understand the functionality of all the code 
# and respond its understanding, while chat() will return the "message" for
# this session. You can permanently save this "message" and carry it in each
# subsequent interaction to ensure that GPT understands the context.

# The last element in "messages" is the latest reply of GPT.

def chat(prompt, function, context):
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
    
    init_prompt = "I want to optimize the control structures of the decompiled code and have designed some optimization strategies. Next, I will present the optimization strategies I have developed, followed by the function to be optimized. This function is one from the binary you learned about earlier. Based on the functionality of the previously understood binary and the current function, please determine whether this optimization strategy is applicable for optimizing this function. You can consider this from the perspective of code complexity, or whether you would use a different approach provided in the optimization strategy to write a function with the same functionality. Please analyze each relevant control statement; if it cannot be optimized, answer No. If it can be optimized, answer Yes and provide the method of optimization."
    
    prompt = f"{init_prompt}\nOptimization:\n{prompt}\nCode:\n{function}"

    messages = []
    messages.extend(context)
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
    
    return full_response

