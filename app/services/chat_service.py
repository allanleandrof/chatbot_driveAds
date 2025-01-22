import openai
from config.settings import Config

class ChatService:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.system_message = {
            "role": "system",
            "content": (
                "Você é Rodrigo, o Gestor de Frotas da empresa DriveAds. "
                # ... (rest of the system message)
            )
        }
    
    def get_chat_response(self, conversation_history):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation_history
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            raise Exception(f"Error getting chat response: {str(e)}")