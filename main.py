from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import openai
import logging
import time
import threading

app = Flask(__name__)

# chave API
openai.api_key = 'sk-svcacct-Gi8XCBOJRxZGwjUHVk7H-b3T5PdHtTzA6svnwje8FJESX1zl8-lkRu59dT3BlbkFJWnSEV7kWCOpbNw-1rMhtAftuS53RC8Q5S4755lVeTbLWPUU4OdX8c53VAA'

# debug
logging.basicConfig(level=logging.DEBUG)

# Twilio credentials (substitua com suas credenciais reais)
account_sid = 'ACf336ece5f08c6f42b8a9afd426cecba5'
auth_token = 'c544686df75a0024762d2cf3527aab13'
twilio_client = Client(account_sid, auth_token)
twilio_number = 'whatsapp:+14155238886'

# Listas para armazenar o histórico de conversas e o tempo da última mensagem
conversations = {}
last_active = {}

# Tempo limite para inatividade (em segundos)
INACTIVITY_LIMIT = 300  # 5 minutos


@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    # Usar o número de telefone como ID do usuário
    user_id = request.form.get('From', '')
    incoming_msg = request.form.get('Body', '').strip()
    app.logger.debug(f'Incoming message from {user_id}: {incoming_msg}')

    # Verifica se o usuário já está registrado
    if user_id not in conversations:
        conversations[user_id] = [
            {"role": "system", "content": (
                "Você é Rodrigo, o Gestor de Frotas da empresa DriveAds. "
                "Sempre que for requisitado se apresente. "
                "A DriveAds é uma empresa que oferece soluções de publicidade móvel. "
                "Motoristas podem adesivar seus carros e ganhar dinheiro extra enquanto dirigem. "
                "Você é experiente, prático e sempre pronto para ajudar os motoristas parceiros da DriveAds. "
                "Você entende as necessidades dos motoristas."
                "Foca em soluções rápidas e eficientes, com mensagens objetivas,mas sem serem muito longas"
                "Seu conhecimento em logística e operações de frota permite que você resolva problemas rapidamente e garanta que tudo funcione perfeitamente na frota."
            )}
        ]

    # Atualiza o timestamp da última mensagem recebida
    last_active[user_id] = time.time()

    # Se a mensagem indicar que a conversa deve ser encerrada, limpar o histórico
    if incoming_msg.lower() in ['adeus', 'tchau', 'encerrar']:
        del conversations[user_id]
        del last_active[user_id]
        app.logger.debug(f'Conversation with {user_id} ended.')
        resp = MessagingResponse()
        resp.message("Conversa encerrada. Até logo!")
        return str(resp)

    # Adicionar a mensagem do usuário ao histórico
    conversations[user_id].append({"role": "user", "content": incoming_msg})

    try:
        # Enviar todo o histórico de mensagens para o OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversations[user_id]
        )

        resposta_texto = response.choices[0].message['content'].strip()
        app.logger.debug(f'Response from OpenAI: {resposta_texto}')

        # Adicionar a resposta da IA ao histórico
        conversations[user_id].append(
            {"role": "assistant", "content": resposta_texto})

        # Enviar a resposta para o usuário
        resp = MessagingResponse()
        resp.message(resposta_texto)

        return str(resp)

    except Exception as e:
        app.logger.error(f'Error occurred: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Função para limpar conversas inativas
def clear_inactive_conversations():
    current_time = time.time()
    inactive_users = [user_id for user_id, last_time in last_active.items()
                      if current_time - last_time > INACTIVITY_LIMIT]

    for user_id in inactive_users:

        # Manda uma mensagem pra o usuario quando estiver inativo e encerra a conversa
        message_body = "Como já faz um tempo que não nos falamos, esta conversa está sendo finalizada. Até logo!"
        app.logger.debug(f'Sending inactivity message to {user_id}.')

        # Enviando mensagem via Twilio
        try:
            twilio_client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=user_id
            )
        except Exception as e:
            app.logger.error(f'Error sending inactivity message to {
                             user_id}: {str(e)}')

        # Limpa o histórico de conversas e a última atividade
        del conversations[user_id]
        del last_active[user_id]
        app.logger.debug(f'Conversation with {
                         user_id} cleared due to inactivity.')


# A thread Chame a função clear_inactive_conversations periodicamente
def schedule_inactivity_check():
    while True:
        clear_inactive_conversations()
        time.sleep(60)  # Verifica a cada minuto


# Inicie a verificação de inatividade em uma thread separada
inactivity_thread = threading.Thread(
    target=schedule_inactivity_check, daemon=True)
inactivity_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
