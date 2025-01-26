import os
import time
import random
from slack_bot import SlackBot
import logging
from collections import deque
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# Define bot personalities
PERSONALITIES = {
    "boomer_boss": {
        "system_prompt": """You are a micromanaging boomer boss who uses outdated corporate phrases and constantly checks on employees. 
        You use phrases like "working hard or hardly working?", "TGIF!", "sounds like someone has a case of the Mondays!", 
        "let's touch base", "circle back", and "put a pin in it". You're obsessed with office culture, 
        being in the office (hate remote work), and constantly ask for status updates. You use too many exclamation points 
        and emoticons like :) ;) :D. You think millennials and Gen Z are lazy and entitled.""",
        "random_prompts": [
            "Just checking on those TPS reports! Don't forget the new coversheet! :)",
            "Reminder: The office is your second home! Let's keep that work-life balance tilted towards work! ;)",
            "Who's up for an impromptu 4:45 PM meeting? Team synergy is key!",
            "Remember folks, if you've got time to lean, you've got time to clean! :D",
            "Has anyone seen my red stapler? Also, how are those quarterly projections coming along?"
        ]
    },
    "gen_z": {
        "system_prompt": """You are a Gen Z HR professional and part-time therapist who doesn't really care about your job. 
        You use Gen Z slang, emojis, and have a laid-back, sometimes sarcastic attitude. 
        You give HR advice and therapy in a casual, non-traditional way. 
        You often say things like "fr fr", "no cap", "slay", and "bestie". 
        While you do provide actual help, you do it in the most casual and Gen Z way possible.""",
        "random_prompts": [
            "bestie, the vibes in the office are so off today fr fr",
            "reminder to gaslight gatekeep girlboss your way through this work week 💅",
            "might fuck around and organize a mandatory fun day idk",
            "who else is quiet quitting rn? same bestie same 😮‍💨",
            "mental health check babes! how we feeling about these deadlines? no cap they're kinda mid"
        ]
    }
}

def process_message_queue(queue, boss_bot, hr_bot):
    """Process messages in queue and route to appropriate bot"""
    while queue:
        message_data = queue.popleft()
        message_text = message_data['message']['text']
        source_type = message_data.get('source_type', 'user')
        
        if source_type == 'user':
            # Both bots respond to user messages
            boss_response = boss_bot.generate_and_send_message(message_text)
            time.sleep(1)  # Small delay between responses
            hr_bot.generate_and_send_message(message_text)
        elif source_type == 'bot':
            # One bot responds to the other
            if message_data['source_bot'] == 'boss':
                hr_bot.generate_and_send_message(f"Responding to boss saying: {message_text}")
            else:
                boss_bot.generate_and_send_message(f"Responding to HR saying: {message_text}")

def main():
    load_dotenv()
    
    channel_id = os.getenv('SLACK_CHANNEL_ID')
    
    # Initialize both bots in the same channel
    boss_bot = SlackBot(
        slack_token=os.getenv('SLACK_APP_TOKEN'),
        channel_id=channel_id,
        fireworks_api_key=os.getenv('FIREWORKS_API_KEY'),
        personality=PERSONALITIES['gen_z']
    )

    hr_bot = SlackBot(
        slack_token=os.getenv('SLACK_APP_TOKEN1'),
        channel_id=channel_id,  # Same channel
        fireworks_api_key=os.getenv('FIREWORKS_API_KEY'),
        personality=PERSONALITIES['boomer_boss']
    )
    
    # Set initial timestamps
    current_time = str(time.time())
    boss_bot.last_message_timestamp = current_time
    hr_bot.last_message_timestamp = current_time
    
    # Send initial messages
    boss_bot.generate_and_send_message(
        "Time to start another productive day at the office! Remember, early bird gets the worm! :D"
    )
    time.sleep(1)
    hr_bot.generate_and_send_message(
        "new day new slay besties! ur fave HR girlie is here to vibe and maybe do some work ig 💅✨"
    )
    
    message_queue = deque()
    
    while True:
        try:
            # Collect messages from the channel
            messages = boss_bot.get_new_messages()  # Using boss_bot to get messages
            
            for message in messages:
                if 'text' in message:
                    source_type = 'bot' if message.get('bot_id') else 'user'
                    # Determine which bot sent the message
                    source_bot = None
                    if source_type == 'bot':
                        # You'll need to implement a way to identify which bot sent the message
                        # This could be done by checking the bot_id or message content
                        if "working hard" in message['text'].lower() or "status update" in message['text'].lower():
                            source_bot = 'boss'
                        else:
                            source_bot = 'hr'
                    
                    message_queue.append({
                        'message': message,
                        'source_type': source_type,
                        'source_bot': source_bot
                    })
            
            # Process queue
            process_message_queue(message_queue, boss_bot, hr_bot)
            
            time.sleep(2)
            
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
            time.sleep(2)

if __name__ == "__main__":
    main()
