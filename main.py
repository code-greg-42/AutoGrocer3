from classes.AutoGrocer_Agent import AutoGrocer_Agent
from utils.print_messages import autogrocer_title

def main():
    
    # print the program header
    
    print(autogrocer_title)
    # get username from user; affect aws_bucket_name
    username = input("USERNAME: ")
    
    # instantiate AutoGrocer_Agent with username
    chatbot_agent = AutoGrocer_Agent(username)
    
    while True:
        
        # run a single chatbot agent cycle
        chatbot_agent.run_single_agent_cycle()
        
        # check if the user wants to exit the program
        if chatbot_agent.next_task == 'quit':
            break
