import os
import time
import random
from slack_bot import SlackBot
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize both bots with different personalities
    bot = SlackBot(
        slack_token=os.getenv('SLACK_APP_TOKEN'),
        channel_id=os.getenv('SLACK_CHANNEL_ID'),
        fireworks_api_key=os.getenv('FIREWORKS_API_KEY')
    )

    bot1 = SlackBot(
        slack_token=os.getenv('SLACK_APP_TOKEN1'),
        channel_id=os.getenv('SLACK_CHANNEL_ID1'),
        fireworks_api_key=os.getenv('FIREWORKS_API_KEY')
    )
    
    # Send initial messages
    bot.send_message("Heyyy bestie! Your fave HR girlboss is here and ready to slay! 💅✨")
    bot1.send_message("Good morning team! Just checking in to make sure everyone's giving 110% today! :D")
    
    # Set timestamps for both bots
    current_time = time.time()
    bot.last_message_timestamp = str(current_time)
    bot1.last_message_timestamp = str(current_time)
    
    # Continuous monitoring loop
    while True:
        try:
            # Handle bot messages
            new_messages = bot.get_new_messages()
            for message in new_messages:
                if 'text' in message:
                    logging.info(f"Received message in channel 1: {message['text']}")
                    bot.generate_and_send_message(message['text'], personality="gen_z")
            
            # Handle bot1 messages
            new_messages1 = bot1.get_new_messages()
            for message in new_messages1:
                if 'text' in message:
                    logging.info(f"Received message in channel 2: {message['text']}")
                    bot1.generate_and_send_message(message['text'], personality="boomer_boss")
            
            # Random micromanaging messages from bot1
            if random.random() < 0.1:  # 10% chance every cycle
                micromanage_prompts = [
                    "Just wanted to check on that status report! Where are we at with that?",
                    "Hope everyone's being productive! Remember, coffee is for closers! ;)",
                    "Can we schedule a quick sync to align on deliverables?",
                    "Working hard or hardly working, team? :D",
                    "Let's circle back on those action items from yesterday's meeting!"
                ]
                bot1.generate_and_send_message(random.choice(micromanage_prompts), personality="boomer_boss")
            
            time.sleep(2)
            
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
            time.sleep(2)

if __name__ == "__main__":
    main()
