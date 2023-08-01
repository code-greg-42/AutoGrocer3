import time
import json
from utils.openai_utils import gpt4_chat_call, gpt3_categorize_msg, generate_photo
from utils.authenticate_all import auth_all
from utils.text_processing import extract_url
from utils.get_text_from_url import get_text_from_url
from utils.print_messages import autogrocer_agent_print

# TODO: add username somewhere in the data being passed to the gpt-4 model to get more interesting responses and welcome messages

# main flow is one single cycle of: request task, perform task, attach response to chat history
class AutoGrocer_Agent:
    
    def __init__(self, _username, _use_twilio=False):
        
        print("Connecting to AutoGrocer Agent...")
        # use the user name to initialize the agent and aws storage
        self.username = _username
        auth_vars = auth_all(_username, _use_twilio)
        # initialize all auth variables
        self.chat_history = auth_vars['chat_history']
        self.aws_s3_client = auth_vars['aws_s3_client']
        self.aws_bucket_name = auth_vars['aws_bucket_name']
        self.google_cloud_client = auth_vars['google_cloud_client']
        self.twilio_client = auth_vars['twilio_client']
        # placeholder for next task, recent_user_input, and recent_gpt_response
        self.next_task = None
        self.recent_user_input = None
        self.recent_gpt_response = None
        print("AutoGrocer Agent connected!")
        print(f"Welcome to the AutoGrocer Chatbot Interface, {_username}!")
        self.print_menu()
    
    def add_to_chat_history(self, _role, _message):
        self.chat_history.append({"role": _role, "content": _message})
        
    def chat_conversation(self):
        try:
            gpt_response = gpt4_chat_call('chat_conversation', self.chat_history)
            self.recent_gpt_response = gpt_response
            self.add_to_chat_history("assistant", gpt_response)
            
        except Exception as e:
            print(e)
    
    # uses gpt-3.5-turbo to categorize the user input message and determine the next task
    def determine_next_task(self):
        
        url_in_message = extract_url(self.recent_user_input)
    
        if url_in_message:
            self.recipe_details_from_url(url_in_message)
        
        else:
            self.add_to_chat_history("user", self.recent_user_input)
            next_step_choice = gpt3_categorize_msg(self.chat_history)
            
            # run it one more time if gpt3_categorize_msg returns 'none' (adds robustness to the program)
            if next_step_choice == 'none':
                next_step_choice = gpt3_categorize_msg(self.chat_history)

        self.next_task = next_step_choice
    
    # executes self.next_task
    # TODO: add a task to view the menu or the chat history
    def execute_next_task(self):
        
        match self.next_task:
            
            case 'recipe_inventory':
                self.view_inventory('recipe')
            case 'pantry_inventory':
                self.view_inventory('pantry')
            case 'chat_conversation':
                self.chat_conversation()
            case 'recommend_recipe':
                self.recommend_recipe()
            case 'generate_shopping_list':
                self.generate_shopping_list()
            case 'quit':
                print('Cook Tim: Thanks for chatting with me today. I hope I was able to help! See you next time!')
            case _:
                print("Cook Tim: Sorry, I didn't understand that. Please double check your message and try again.")
    
    # utility function to create an image of a food item or recipe and save it to storage ### max 20 characters
    def generate_photo(self, item_description_prompt):
        photo_url = generate_photo(item_description_prompt[:20])
        self.store_item('food_photo', photo_url)
    
    # TODO: copy over the function to generate a shopping list from a recipe --- will require store inventory, total_required_ingredients, and pantry inventory
    def generate_shopping_list(self):
        print("Cook Tim: This feature will be added soon. Please check back later.")
    
    # TODO: copy over the function to gather the store inventory by webscraping the store website
    def get_store_inventory(self):
        pass
    
    def get_user_input(self):
        self.recent_user_input = input(f"{self.username}: ")
        
    def print_menu(self):
        print(autogrocer_agent_print)
    
    def recipe_details_from_url(self, _url):
        raw_recipe_text = get_text_from_url(self.google_cloud_client, _url)
        recipe_details = gpt4_chat_call('extract', raw_recipe_text)
        self.store_item('recipe', recipe_details)
        
    # TODO: add print statement for recipe details to be displayed to user
    def recommend_recipe(self):
        recipe_details = gpt4_chat_call('recommend', self.chat_history)
        self.store_item('recipe', recipe_details)
        # add print statements for user to see basic recipe details
    
    # inputs a user message and runs a full cycle of the AutoGrocer Agent
    # flow: user input >> determine next task >> execute next task >> return response
    def run_single_agent_cycle(self):
        
        self.recent_user_input = self.get_user_input()
        
        # user input message is added to chat history in determine_next_task
        self.determine_next_task(self.recent_user_input)
        
        # any gpt response messages are added to chat history in execute_next_task
        self.execute_next_task()
        
    # types: recipe, pantry, food_photo
    def store_item(self, _type, _content):
        if _type == 'food_photo':
            self.aws_s3_client.put_object(Bucket=self.aws_bucket_name, Key=f'food_photo_{_content}_{str(time.time())[-5:]}.txt', Body=_content)
        elif _type in ['recipe', 'pantry']:
            self.aws_s3_client.put_object(Bucket=self.aws_bucket_name, Key=f'{_type}_{str(time.time())[-7:]}.txt', Body=_content) 
        else:
            print("Something went wrong. Please try again.")
    
    # types: recipe, pantry    
    def view_inventory(self, _type):
        
        bucket_file_list = self.aws_s3_client.list_objects_v2(Bucket=self.aws_bucket_name, Prefix=f'{_type}_')
        if bucket_file_list['KeyCount'] == 0:
            print(f"Cook Tim: You don't have any {'recipes' if _type == 'recipe' else 'pantry items'} in your {_type} inventory yet. Would you like to add one? (y/n)\n")
            return False
        for i, _file in enumerate(bucket_file_list['Contents']):
            _file_contents = self.aws_s3_client.get_object(Bucket=self.aws_bucket_name, Key=_file['Key'])
            file_details = json.loads(_file_contents['Body'].read().decode('utf-8'))
            if _type == 'recipe':
                print(f"{i+1}. {file_details['name']}")    
            else:
                pantry_item = _file_contents['Body'].read().decode('utf-8')
                print(f"{i+1}. {pantry_item['name']}: {pantry_item['quantity']} {pantry_item['unit']}")
        return True

