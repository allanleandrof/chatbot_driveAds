# DriveAds WhatsApp Bot API Documentation

## Overview

The DriveAds WhatsApp Bot API is a Flask-based application that provides an automated chat interface for DriveAds drivers through WhatsApp. The bot, named Rodrigo, acts as a Fleet Manager and helps drivers with registration, inquiries, and support.

## Technical Architecture

### Project Structure
```
/driveads_bot
    ├── config/               # Configuration settings
    ├── app/                  # Main application code
    │   ├── routes/          # API endpoints
    │   ├── services/        # Business logic services
    │   └── utils/           # Utility functions
    ├── instance/            # Instance-specific config
    └── requirements.txt     # Project dependencies
```

### Core Components

1. **WhatsApp Integration (Twilio)**
   - Handles incoming and outgoing WhatsApp messages
   - Manages message formatting and delivery

2. **Chat Engine (OpenAI GPT-3.5)**
   - Processes natural language inputs
   - Generates contextual responses
   - Maintains conversation flow

3. **Database (Firebase)**
   - Stores driver information
   - Manages CPF verification
   - Tracks registration status

4. **Conversation Management**
   - Handles conversation state
   - Manages session timeouts
   - Implements cleanup procedures

## API Endpoints

### WhatsApp Webhook
```
POST /whatsapp
```

Handles incoming WhatsApp messages and returns appropriate responses.

#### Request

```json
{
  "From": "whatsapp:+1234567890",
  "Body": "message content"
}
```

#### Response

Returns a TwiML response containing the bot's message.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Bot response message</Message>
</Response>
```

## Services

### ChatService

Manages interactions with OpenAI's GPT-3.5 model.

```python
chat_service.get_chat_response(conversation_history)
```

### FirebaseService

Handles database operations and CPF verification.

```python
firebase_service.check_cpf_exists(cpf)
```

### TwilioService

Manages WhatsApp message sending and receiving.

```python
twilio_service.send_message(to, body)
twilio_service.create_response(message)
```

## Configuration

### Environment Variables

Create a `.env` file in the `instance/` directory with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_NUMBER=your_twilio_whatsapp_number
FIREBASE_CREDENTIALS_PATH=path_to_firebase_credentials
```

### Constants

```python
INACTIVITY_LIMIT = 40  # Conversation timeout in seconds
```

## Error Handling

The API implements error handling for:
- Invalid CPF formats
- OpenAI API failures
- Twilio messaging errors
- Firebase connection issues
- Conversation timeout scenarios

### Error Response Format

```json
{
  "status": "error",
  "message": "Error description"
}
```

## Conversation Flow

1. **Initial Contact**
   - Bot introduces itself as Rodrigo
   - Explains DriveAds service
   - Ready to assist with registration

2. **Registration Process**
   - Requests CPF
   - Verifies existing registration
   - Guides through app download and setup

3. **Conversation Management**
   - Tracks user activity
   - Implements 40-second timeout
   - Sends timeout notification
   - Cleans up inactive sessions

## Security Considerations

1. **Authentication**
   - Twilio webhook authentication
   - Firebase secure credentials
   - OpenAI API key protection

2. **Data Protection**
   - CPF validation
   - Secure storage in Firebase
   - Session management

## Deployment

### Requirements

- Python 3.7+
- Flask
- Firebase Admin SDK
- OpenAI API access
- Twilio account
- Required Python packages (see requirements.txt)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables
4. Run the application:
   ```bash
   python run.py
   ```
   
