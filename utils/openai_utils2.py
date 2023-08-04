import json
import openai
 
function_definition = [{
    "name": "did_user_request_recipe_save",
        "description": "takes a 'yes' or 'no' input regarding whether or not the user wants to save a recipe.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_requested_recipe_save": {
                    "type": "string",
                    "enum": ["yes", "no"],
                    "description": "Your 'yes' or 'no' answer to whether or not the user wants to save a recipe."
                }},
            "required": ["user_requested_recipe_save"]
        }}]


def did_user_request_recipe_save(chat_history):
        _messages = [{
            "role": "assistant",
            "content": "Would you like me to save this recipe to your inventory?",
        },
        {
            "role": "user",
            "content": "sure, that'd be great!"
        }]
        
        _prompt = """
Based on the most recent messages (the end of the array) in the following chat history, please answer this question:
Does the user want to save a recipe? Answer 'yes' or 'no'.

Chat History: """ + json.dumps(_messages)[-2000:]
        
        sys_prompt = "You are in charge of determining whether or not the user wants to save a recipe, based on recent chat history. Please answer 'yes' or 'no'. "
        
        _messages_ready = [{
            "role": "system",
            "content": sys_prompt
        },
        {
            "role": "user",
            "content": _prompt
        }]
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=_messages_ready,
        functions=test_function,
        function_call={"name": 'did_user_request_recipe_save'},
    )
        
        print(response)
        
        return json.loads(response['choices'][0]['message']['function_call']['arguments'])['user_requested_recipe_save']


print(gpt_test()) 