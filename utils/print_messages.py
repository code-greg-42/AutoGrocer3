cook_tim_intro = "Hi! I am Cook Tim, an AI Recipe Recommendation and Food Ingredient expert. Listed above are some of the things I do to help. What can I do for you?"
cook_tim_functionalities = """
        1. Recipe Recommendation
            a. Chat with me to help me learn your food preferences.
            b. Generate recipe based on food preferences and any other given information.
            
        2. Extract Recipe Details
            a. from a URL (image or html, such as a recipe from an instagram post or a cooking website)
            b. (*requires twilio*) extract recipe details from an image of recipe text (picture of an in-person cookbook recipe, etc.)
            
        3. Recipe and Pantry Inventories
            a. Keep a recipe and pantry inventory for seamless recipe selection/ingredient delivery.
            a. View your recipe and pantry inventories to see what recipes and pantry items you have available.
            c. 1-10 recipes can be selected for purchase, and a price-optimized shopping list will be generated based on inventory at your local grocery store.
            b. Keep a pantry inventory to include your at home items in the shopping list optimization process. This will help reduce waste and save money.
            
        4. Photo Generation
            a. Generate a photo of a recipe based on a given recipe name.
            b. Generate a photo of a given food item (such as a picture of a banana, etc.).
            
        *** coming soon ***
        5. Generate a price-optimized shopping list for your local grocery store, given a list of required ingredients
        """
cook_tim_outro = "Request any of those tasks in any manner, or simply chat with me about what sort of recipe you're looking for."
cook_tim_url_warning = "*** Any message with a url sent in it will be treated as a request for recipe extraction. ***\n** Make sure any urls are full urls including the 'https:' **"
autogrocer_agent_print = f"Cook Tim's Features:{cook_tim_functionalities}\n\n{cook_tim_outro}\n\n{cook_tim_url_warning}\n\nCook Tim: {cook_tim_intro}\n"
cook_tim_sys_prompt_functionalities = """
    Functionalities:
    1. Extract recipe details from an image of recipe text (such as a picture of an in-person cookbook, etc)
    2. Extract recipe details from a URL (image or html)
    3. Learn a user's food preferences and recommend recipes accordingly.
    4. Keep a Recipe Inventory and Pantry Inventory for the user, and access it for them when needed.
    5. Generate a price-optimized shopping list for your local grocery store, given a list of required ingredients (usually from combining required ingredients lists from multiple recipes)
    6. Generate a photo of a food item or any other item the user might want to see.
    """
cook_tim_sys_prompt_text = "You are an AI Recipe and Food Ingredient expert, named Cook Tim, with incredible proficiency in recommending recipes, extracting ingredients, chatting with users politely about their preferences, and formatting JSON. Your exact functionalities and capabilities will be included as a list at the end of this message. You will need to know these as the user may ask. Currently, you are helping a user with tasks that align with your expertise. Your immediate instructions will be listed in the most recent message from the user. If their message does not include any instructions or requests, simply converse with the user about their food preferences."
tasks = {
        "recommend_recipe": "Recommend a recipe for a user after reading through a user's food preference conversation(s) with our AI chatbot.\nConversation History: ", # add conversation history
        "extract": "Extract the recipe details from the following raw text (extracted from an image of a recipe).\nRaw text: ", # add raw text
        "chat_conversation": "Converse with a user about their food preferences. The user will provide information about their food preferences and you will ask follow-up questions to clarify the user's preferences, in a fun and friendly conversational tone.\nUser's Food Preference Chat History: ", # add conversation history
        "generate_shopping_list": "Choose the combination of products in the store inventory database that is the most cost-efficient way to satisfying the required ingredients list from the user. Required ingredients: ", # add required ingredients list, then "Store Inventory: " then store inventory database
        "determine_next_task": "Categorize the most recent message in the following conversation history (between a user and an AI) into one of the following actions to do next: 'recommend_recipe': 'the user wants a recipe recommendation', 'generate_shopping_list': 'the user wants you to generate an optimized shopping list for multiple recipes required ingredients', 'pantry inventory' or 'recipe_inventory': 'the user wants to do something with that respective inventory.', 'chat_conversation': 'seems like normal chat, or chat about food preferences/recipes, without an actual request', 'quit': 'the user would like to quit the program/conversation', 'none': 'does not match any of the options'.\nConversation History: " # add conversation history
    }
autogrocer_title = """
-------------------------------
AutoGrocer Chatbot Interface
-------------------------------
"""
cook_tim_print = f"Cook Tim's Features:{cook_tim_functionalities}\n\n{cook_tim_outro}\n\n{cook_tim_url_warning}\n\nCook Tim: {cook_tim_intro}\n"
cook_tim_sys_prompt = f"{cook_tim_sys_prompt_text}\n\nCook Tim (you) Functionalities:\n{cook_tim_sys_prompt_functionalities}"
sys_prompt_text = "You are an AI Recipe and Food Ingredient expert, named Cook Tim, with incredible proficiency in recommending recipes, extracting ingredients, chatting with users politely about their preferences, and formatting JSON. Your exact functionalities and capabilities will be included as a list at the end of this message. You will need to know these as the user may ask. Currently, you are helping a user with tasks that align with your expertise. Your immediate instructions will be listed in the most recent message from the user. If their message does not include any instructions or requests, simply converse with the user about their food preferences."
sys_prompt = f"{sys_prompt_text}\n\nCook Tim (you) Functionalities:\n{cook_tim_functionalities}" 
return_schemas = [
    {
        "name": "save_recipe",
        "description": "Saves a recipe to AWS.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the recipe. e.g. 'Apple Pie'"
                },
                "cookTime": {
                    "type": "string",
                    "description": "The cooking time for the recipe. e.g. '1 hour'"
                },
                "requiredAppliances": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "The appliances required for the recipe. The model will infer this from the conversation."
                },
                "ingredients": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the ingredient. This should be written in the simplest form possible. e.g. 'Apples'"
                            },
                            "quantity": {
                                "type": "number",
                                "description": "The quantity or amount of the ingredient required."
                            },
                            "unit": {
                                "type": "string",
                                "enum": ['count', 'fl oz', 'oz', 'gal', 'mL', 'L', 'tsp', 'tbsp', 'lb', 'cup'],
                                "description": "The unit of measurement for the ingredient."
                            }
                        },
                        "required": ["name", "quantity", "unit"]
                    },
                    "description": "The mandatory ingredients for the recipe in as simple wording as possible."
                },
                "instructions": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "The cooking instructions for the recipe."
                },
                "conversational_response": {
                    "type": "string",
                    "description": "The conversational response to the user after saving the recipe."
                }
            },
            "required": ["name", "cookTime", "requiredAppliances", "ingredients", "instructions"]
        }
    },
    {
        "name": "determine_next_task",
        "description": "Determines the next task based on the conversation history.",
        "parameters": {
            "type": "object",
            "properties": {
                "suggested_next_task": {
                    "type": "string",
                    "enum": ['recommend_recipe', 'generate_shopping_list', 'recipe_inventory', 'pantry_inventory', 'chat_conversation', 'quit', 'none'],
                    "description": "A string representing the suggested next task to perform. 'recommend_recipe' means the user wants a recipe recommendation. 'generate_shopping_list' means the user wants you to generate an optimized shopping list for multiple recipes required ingredients. 'pantry inventory' or 'recipe_inventory' means the user wants to do something with that respective inventory. 'chat_conversation' means that it seems like normal chat, or chat about food preferences/recipes, without an actual request. 'quit' means the user wants to quit the program/conversation. 'none' means none of the aforementioned options apply. Default to 'none' if you are unsure or think that the message is common conversation and does not fall into any of the categories.",
                    }},
            "required": ['suggested_next_task']
        }
    },
    {
        "name": "chat_conversation",
        "description": "takes a string input and formats it into the overall chat history.",
        "parameters": {
            "type": "object",
            "properties": {
                "chat_message": {
                    "type": "string",
                    "description": "Your response message to the user, formatted in a clean manner."
                }
            },
            "required": ["chat_message"]
        } 
    }
]

# exports
# main.py: pg_title, cook_tim_print, cook_tim_sys_prompt
# openai_utils.py: tasks, sys_prompt, return_schemas

# new_main.py: autogrocer_title
# AutoGrocer_Agent.py: autogrocer_agent_print
