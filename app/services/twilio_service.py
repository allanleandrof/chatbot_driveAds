from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from config.settings import Config

class TwilioService:
    def __init__(self):
        self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        self.twilio_number = Config.TWILIO_NUMBER
    
    def send_message(self, to, body):
        try:
            self.client.messages.create(
                body=body,
                from_=self.twilio_number,
                to=to
            )
        except Exception as e:
            raise Exception(f"Error sending Twilio message: {str(e)}")
    
    def create_response(self, message):
        resp = MessagingResponse()
        resp.message(message)
        return str(resp)