# Virtual Gynecology Chatbot

A virtual gynecology assistant powered by multiple AI models (ChatGPT, Gemini, and Grok) with a Chainlit frontend and Django backend.

## Project Overview

This project is a gynecology chatbot that provides users with information and guidance about gynecological health concerns. It features:

- **Multiple AI Models**: Get responses from ChatGPT, Gemini, and Grok
- **Side-by-Side Comparison**: Compare responses from different models
- **User-Friendly Interface**: Simple chat interface built with Chainlit

## Tech Stack

- **Frontend**: Chainlit (Python-based UI framework)
- **Backend**: Django (REST API)
- **AI Models**:
  - OpenAI's GPT models
  - Google's Gemini models
  - xAI's Grok models (simulated in current implementation)

## Directory Structure

```
gynecology_chatbot/
├── backend/                      # Existing Django backend
│   ├── gynecology_chatbot_project/
│   ├── users/
│   ├── chatbot/
│   ├── doctors/
│   ├── manage.py
│   └── requirements.txt
├── chainlit_app/                 # New Chainlit frontend
│   ├── app.py                    # Main Chainlit application
│   ├── config.py                 # Configuration and environment variables
│   ├── models/                   # LLM integrations
│   ├── components/               # UI components
│   ├── static/                   # CSS and other static files
│   ├── chainlit.md               # Welcome message
│   ├── .env                      # Environment variables for API keys
│   └── requirements.txt          # Chainlit app dependencies
└── README.md                     # Project documentation
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (for the Django backend)
- API keys for:
  - OpenAI
  - Google AI (Gemini)
  - Grok (when available)

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/peca-ai-code/congenial-winner.git
   cd congenial-winner
   ```

2. **Set up the Django backend** (optional - not required for basic Chainlit functionality):
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Configure .env file with database settings
   
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

3. **Set up the Chainlit frontend**:
   ```bash
   cd chainlit_app
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Configure .env file with API keys
   ```

4. **Run the Chainlit app**:
   ```bash
   chainlit run app.py
   ```

5. **Open the application in your browser**:
   - The Chainlit app will be available at [http://localhost:8000](http://localhost:8000)

## Configuration

### Environment Variables

Create a `.env` file in the `chainlit_app` directory with the following variables:

```
# API Keys for AI models
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key
GROK_API_KEY=your-grok-api-key

# Model Configuration
OPENAI_MODEL=gpt-4
GEMINI_MODEL=gemini-pro
GROK_MODEL=grok-1
```

## Features

### 1. Multi-Model Responses

- Each user query is sent to multiple AI models
- The primary model (selectable by the user) provides the main response
- All model responses are available for comparison

### 2. Side-by-Side Comparison

- Toggle comparison view on/off in settings
- Compare how different models respond to the same query
- Identify differences in information and approach

### 3. Medical Context

- All models are provided with the same gynecology-specific system prompt
- Responses emphasize when to seek professional medical advice
- Models avoid providing definitive diagnoses

## Usage

1. Start a new chat session
2. Type your gynecological health question or concern
3. Receive responses from multiple AI models
4. Compare responses to get a more comprehensive understanding
5. Change settings to select your preferred primary model

## Important Note

This chat assistant is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## License

[Insert appropriate license information here]

## Acknowledgments

- OpenAI for GPT models
- Google for Gemini models
- xAI for Grok (future integration)
- Chainlit for the UI framework
- Django for the backend framework

## Contact

[Insert contact information here]
