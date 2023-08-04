import json
import openai
from utils.print_messages import return_schemas
from utils.text_processing import format_prompt

def gpt3_categorize_msg(_chat_history):
    
    _messages = format_prompt("determine_next_task", _chat_history)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=_messages,
        functions=return_schemas,
        function_call={"name": "determine_next_task"},
    )
    
    return json.loads(response['choices'][0]['message']['function_call']['arguments'])['suggested_next_task']

def gpt4_chat_call(_type, _content):
    
    _messages = format_prompt(_type, _content)
    print(_messages)
    
    if _type == 'recommend_recipe' or _type == 'extract':
        function_name = 'save_recipe'
    else:
        function_name = _type
        
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=_messages,
        functions=return_schemas,
        function_call={"name": function_name},
    )
    
    gpt_answer = response['choices'][0]['message']['function_call']['arguments']
    
    if type == 'chat_conversation':
        gpt_answer = json.loads(gpt_answer)['chat_message']
        
    return gpt_answer

def generate_photo(_prompt):
    
    # send the prompt to the API
    response = openai.Image.create(
        prompt=_prompt,
        n=1,
        size="256x256",
    )
    
    return response['data'][0]['url']

