import re
import json
from utils.print_messages import tasks, sys_prompt

def extract_url(message):
    url_pattern = '\\b((?:https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:, .;]*[-a-zA-Z0-9+&@#/%=~_|])'
    urls = re.findall(url_pattern, message)
    return urls[0] if urls else None

def format_prompt(_type, _data_to_add):

    if _type == 'generate_shopping_list':
        user_messages = [message['content'] for message in _data_to_add[2] if message['role'] == 'user']
        json_user_messages = json.dumps(user_messages)
        if len(json_user_messages) > 2500:
            json_user_messages = json_user_messages[-2500:]
        content = f"Your Task: {tasks[_type]}{json.dumps(_data_to_add[0])}\n\nStore Inventory: {json.dumps(_data_to_add[1])}\n\nUser Preferences Message History: {json_user_messages}"
        
    elif _type in ['recommend_recipe', 'chat_conversation', 'determine_next_task']:
        user_conversation_only = [f"{message['role']}: {message['content']}" for message in _data_to_add if message['role'] != 'system']
        json_data = json.dumps(user_conversation_only)
        if len(json_data) > 5000:
            json_data = json_data[-5000:]
        content = f"Your Task: {tasks[_type]}{json_data}"
        
    elif _type == 'extract':
        content = f"Your Task: {tasks[_type]}{_data_to_add}"
    else:
        raise ValueError("Invalid type.")
    
    formatted_array = [{
        "role": "system",
        "content": sys_prompt
    },
    {
        "role": "user",
        "content": content
    }]
    
    return formatted_array
