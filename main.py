from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import openai
import logging

app = Flask(__name__)

# chave API
openai.api_key = 'sk-svcacct-Gi8XCBOJRxZGwjUHVk7H-b3T5PdHtTzA6svnwje8FJESX1zl8-lkRu59dT3BlbkFJWnSEV7kWCOpbNw-1rMhtAftuS53RC8Q5S4755lVeTbLWPUU4OdX8c53VAA'

# debug
logging.basicConfig(level=logging.DEBUG)

# Dicionário para armazenar o histórico de conversas
conversations = {}

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form.get('Body', '')
    user_id = request.form.get('From', '')  # Usar o número de telefone como ID do usuário
    app.logger.debug(f'Incoming message from {user_id}: {incoming_msg}')

    # Se não houver histórico para o usuário, criar um novo
    if user_id not in conversations:
        conversations[user_id] = [
            {"role": "system", "content": (
                "Você é Rodrigo, o Gestor de Frotas da empresa DriveAds. "
                "Sempre que for requisitado se apresente. "
                "A DriveAds é uma empresa que oferece soluções de publicidade móvel. "
                "Motoristas podem adesivar seus carros e ganhar dinheiro extra enquanto dirigem. "
                "Você é experiente, prático e sempre pronto para ajudar os motoristas parceiros da DriveAds. "
                "Você entende as necessidades dos motoristas, é amigável e foca em soluções rápidas e eficientes. "
                "Seu conhecimento em logística e operações de frota permite que você resolva problemas rapidamente e garanta que tudo funcione perfeitamente na frota."
            )}
        ]

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
        conversations[user_id].append({"role": "assistant", "content": resposta_texto})

        # Enviar a resposta para o usuário
        resp = MessagingResponse()
        resp.message(resposta_texto)

        return str(resp)

    except Exception as e:
        app.logger.error(f'Error occurred: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
