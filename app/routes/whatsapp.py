from flask import Blueprint, request
from app.services.chat_service import ChatService
from app.services.firebase_service import FirebaseService
from app.services.twilio_service import TwilioService
from app.utils.conversation_manager import ConversationManager

whatsapp_bp = Blueprint('whatsapp', __name__)

chat_service = ChatService()
firebase_service = FirebaseService()
twilio_service = TwilioService()
conversation_manager = ConversationManager(twilio_service)

@whatsapp_bp.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    user_id = request.form.get('From', '')
    incoming_msg = request.form.get('Body', '').strip()
    
    if incoming_msg.lower() in ['adeus', 'tchau', 'encerrar']:
        conversation_manager.clear_conversation(user_id)
        return twilio_service.create_response("Conversa encerrada. Até logo!")
    
    conversation_manager.add_message(user_id, incoming_msg)
    
    if len(incoming_msg) == 11 and incoming_msg.isdigit():
        cpf_exists, nome_motorista = firebase_service.check_cpf_exists(incoming_msg)
        if cpf_exists:
            response_text = (
                f"O CPF informado já está cadastrado no sistema sob o nome de {nome_motorista}. "
                "Por favor, faça login no aplicativo DriveAds para mais informações."
            )
        else:
            response_text = (
                "O CPF informado não está cadastrado. Vamos prosseguir com o seu cadastro. "
                "Por favor, siga as instruções para completar o cadastro."
            )
    else:
        conversation_history = conversation_manager.get_conversation(user_id)
        response_text = chat_service.get_chat_response(conversation_history)
    
    conversation_manager.add_message(user_id, response_text, is_user=False)
    return twilio_service.create_response(response_text)