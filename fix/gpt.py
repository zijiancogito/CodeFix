from openai import OpenAI

# When using API calls to GPT, context needs to be passed through the "message".
# You can change the context of GPT by adjusting the content of the "message".

# In the initial call, GPT will understand the functionality of all the code 
# and respond its understanding, while chat() will return the "message" for
# this session. You can permanently save this "message" and carry it in each
# subsequent interaction to ensure that GPT understands the context.

# The last element in "messages" is the latest reply of GPT.

def chat(prompt, model, messages=[]):
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

    messages.append({"role":"user", "content":prompt})
    init_response = client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model=model,
            messages=messages,
            stream=True,
            )
    full_response = ''

    for chunk in init_response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
    messages.append({"role":"assistant", "content": full_response})
    
    return messages

