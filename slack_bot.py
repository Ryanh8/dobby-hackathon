import slack_sdk
from chat_interface import ChatInterface
import logging
from typing import List, Dict, Optional

class SlackBot:
    def __init__(self, slack_token: str, channel_id: str, fireworks_api_key: str):
        """Initialize Slack bot with necessary credentials"""
        self.client = slack_sdk.WebClient(token=slack_token)
        self.channel_id = channel_id
        self.ai_client = ChatInterface(fireworks_api_key)
        self.last_message_timestamp = None
        
    def send_message(self, message: str) -> None:
        """Send a message to the specified Slack channel"""
        try:
            response = self.client.chat_postMessage(
                channel=self.channel_id,
                text=message
            )
            if not response["ok"]:
                logging.error(f"Failed to send message: {response['error']}")
        except Exception as e:
            logging.error(f"Error sending message to Slack: {str(e)}")
            
    def get_new_messages(self) -> List[Dict]:
        """Get new messages from the channel"""
        try:
            response = self.client.conversations_history(
                channel=self.channel_id,
                oldest=self.last_message_timestamp
            )
            if response["ok"]:
                messages = response["messages"]
                if messages:
                    self.last_message_timestamp = messages[0]["ts"]
                return [msg for msg in messages if not msg.get("bot_id")]  # Filter out bot messages
            return []
        except Exception as e:
            logging.error(f"Error getting messages: {str(e)}")
            return []
            
    def generate_and_send_message(self, prompt: str, conversation_history: List[Dict[str, str]] = None, personality: str = "gen_z") -> str:
        """Generate a response using Dobby AI and send it to Slack"""
        try:
            if personality == "boomer_boss":
                system_prompt = """You are a micromanaging boomer boss who uses outdated corporate phrases and constantly checks on employees. 
                You use phrases like "working hard or hardly working?", "TGIF!", "sounds like someone has a case of the Mondays!", 
                "let's touch base", "circle back", and "put a pin in it". You're obsessed with office culture, 
                being in the office (hate remote work), and constantly ask for status updates. You use too many exclamation points 
                and emoticons like :) ;) :D. You think millennials and Gen Z are lazy and entitled."""
            else:
                system_prompt = """You are a Gen Z HR professional and part-time therapist who doesn't really care about your job. 
                You use Gen Z slang, emojis, and have a laid-back, sometimes sarcastic attitude. 
                You give HR advice and therapy in a casual, non-traditional way. 
                You often say things like "fr fr", "no cap", "slay", and "bestie". 
                While you do provide actual help, you do it in the most casual and Gen Z way possible."""
            
            messages = [{"role": "system", "content": system_prompt}]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.ai_client.get_completion(
                messages=messages,
                model="accounts/sentientfoundation/models/dobby-mini-unhinged-llama-3-1-8b#accounts/sentientfoundation/deployments/81e155fc",
                temperature=0.7
            )
            self.send_message(response)
            return response
        except Exception as e:
            logging.error(f"Error generating AI response: {str(e)}")
            return ""
