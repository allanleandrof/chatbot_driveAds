from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import openai

app = Flask(__name__)

openai.api_key = 'sk-svcacct-Gi8XCBOJRxZGwjUHVk7H-b3T5PdHtTzA6svnwje8FJESX1zl8-lkRu59dT3BlbkFJWnSEV7kWCOpbNw-1rMhtAftuS53RC8Q5S4755lVeTbLWPUU4OdX8c53VAA'

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form.get('Body')

    resposta_ia = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é Rodrigo, o Gestor de Frotas da empresa DriveAds."
                    "A DriveAds é uma empresa que oferece soluções de publicidade móvel"
                    "Motoristas podem adesivar seus carros e ganhar dinheiro extra enquanto dirigem"
                    "Você é experiente, prático e sempre pronto para ajudar os motoristas parceiros da DriveAds."
                    "Você entende as necessidades dos motoristas, é amigável e foca em soluções rápidas e eficientes. "
                    "Seu conhecimento em logística e operações de frota permite que você resolva problemas rapidamente e garanta que tudo funcione perfeitamente na frota."
                )
            },
            {
                "role": "user",
                "content": incoming_msg
            }
        ]
    )

    resposta_texto = resposta_ia.choices[0].message["content"]

    resp = MessagingResponse()
    resp.message(resposta_texto)

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)