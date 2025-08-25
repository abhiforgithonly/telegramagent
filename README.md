# 🤖 AI-Powered Telegram Agent Bot

A sophisticated Telegram bot powered by OpenAI's GPT that provides natural conversation, intelligent responses, and helpful assistance directly in your chat.

## ✨ Features

### 🧠 **AI-Powered Conversations**
- Natural language understanding and response generation
- Context-aware conversations with memory
- Intent analysis (questions, requests, greetings, etc.)
- Sentiment analysis and appropriate response matching

### 💬 **Smart Interaction**
- Maintains conversation history per user
- Contextual responses based on chat history
- Fallback responses when AI is unavailable
- Session tracking and statistics

### 🛠️ **User-Friendly Commands**
- Simple command structure
- Intuitive natural language interface
- Helpful guidance and examples
- Session management features

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key (optional but recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/telegram-agent-bot.git
   cd telegram-agent-bot
   ```

2. **Install dependencies**
   ```bash
   pip install python-telegram-bot aiohttp python-dotenv openai
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   ```

4. **Configure environment variables**
   ```bash
   # .env file
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here  
   ```

5. **Run the bot**
   ```bash
   python final_bot.py
   ```

## 📋 Dependencies

Install these packages using pip:

```bash
pip install python-telegram-bot aiohttp python-dotenv openai
```

**Package Details:**
- `python-telegram-bot` - Telegram Bot API wrapper
- `aiohttp` - Async HTTP client for OpenAI API calls  
- `python-dotenv` - Environment variable management
- `openai` - Official OpenAI Python client (optional but recommended)

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | Your Telegram bot token from @BotFather |
| `OPENAI_API_KEY` | ❌ Optional | OpenAI API key for enhanced AI responses |

### Getting Your Tokens

#### 1. Telegram Bot Token
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command
3. Follow the prompts to create your bot
4. Copy the token provided

#### 2. OpenAI API Key (Optional)
1. Visit [OpenAI API](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Generate a new API key
4. Copy the key to your `.env` file

> **Note:** Without OpenAI API key, the bot will use simple keyword-based responses.

## 📖 Usage

### Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize the bot and start conversation |
| `/help` | Show available commands and examples |
| `/clear` | Clear conversation history for fresh start |
| `/status` | Show your session information and statistics |

### Natural Conversation Examples

Just type naturally! The bot understands:

```
👋 Greetings:
"Hello!", "Hi there!", "Good morning!"

❓ Questions:
"What's the weather like?", "How does AI work?", "Tell me about Python"

🙏 Requests:
"Help me write an email", "Explain quantum physics simply", "Give me coding tips"

💬 Casual Chat:
"Tell me a joke", "How was your day?", "What's interesting about space?"
```

## 🏗️ Architecture

### Core Components

```
telegram_agent_bot.py
├── LLMProcessor          # AI language model integration
│   ├── analyze_intent()  # Message intent and sentiment analysis
│   ├── generate_response() # Contextual response generation
│   └── conversation_history # Per-user context memory
│
└── TelegramAgentBot     # Main bot controller
    ├── Command Handlers  # /start, /help, /clear, /status
    ├── Message Handler   # Natural language processing
    └── Session Management # User session tracking
```

### Data Flow

1. **User Message** → Intent Analysis → Context Retrieval
2. **AI Processing** → Response Generation → History Update
3. **Response Delivery** → Session Update → Logging

## 🔍 Features in Detail

### 🧠 AI Capabilities
- **Intent Recognition**: Understands whether you're asking, requesting, greeting, or chatting
- **Context Awareness**: Remembers previous messages in your conversation
- **Smart Responses**: Generates relevant, helpful responses using GPT-3.5
- **Fallback System**: Works even without AI using keyword-based responses

### 💾 Memory Management
- Keeps last 10 conversation exchanges per user
- Automatic cleanup to prevent memory issues
- Session persistence during bot runtime
- Clear history functionality for privacy

### 📊 Session Tracking
- Message count per user
- Session duration tracking
- Conversation history statistics
- Bot status monitoring

## 🚦 Running the Bot

### Development Mode

**Windows:**
```cmd
# Using Command Prompt
python final_bot.py

# Using PowerShell  
python final_bot.py

# Keep running in background (Windows)
# Use Task Scheduler or run in a separate command window
```

**macOS/Linux:**
```bash
# Direct execution
python3 final_bot.py

# Background execution (keeps running after closing terminal)
nohup python3 final_bot.py &
```

### 💻 Platform-Specific Setup

#### Windows Setup
```cmd
# 1. Install Python from python.org (3.7+)
# 2. Open Command Prompt or PowerShell
cd path\to\your\bot\folder
pip install python-telegram-bot aiohttp python-dotenv openai
python final_bot.py
```

#### macOS Setup  
```bash
# 1. Install Python (if not already installed)
brew install python3

# 2. Setup the bot
cd /path/to/your/bot/folder
pip3 install python-telegram-bot aiohttp python-dotenv openai
python3 final_bot.py
```

### Production Deployment

#### Windows (Background Service)
```batch
# Method 1: Using Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "When the computer starts"
4. Set action to start your Python script
5. Configure to run whether user is logged in or not

# Method 2: Using NSSM (Non-Sucking Service Manager)
# Download NSSM from https://nssm.cc/
nssm install TelegramBot
# Point to your Python executable and script
# Service will start automatically
```

#### macOS (Background Service)
```bash
# Create launch daemon
~/Library/LaunchAgents/com.telegrambot.plist

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.telegrambot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/your/telegram_agent_bot.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>

# Load the service
launchctl load ~/Library/LaunchAgents/com.telegrambot.plist
```

#### Cloud Hosting (Recommended)
For 24/7 operation without keeping your computer on:

**Free Options:**
- **Render.com**: Free tier with automatic deploys
- **Railway.app**: Simple deployment from GitHub
- **Fly.io**: Free allowance for small apps

**Paid Options:**
- **Heroku**: Easy deployment ($7/month)  
- **DigitalOcean**: VPS starting at $5/month
- **AWS/Google Cloud**: Pay-as-you-use

## 🐛 Troubleshooting

### Common Issues

#### Bot Not Responding
```bash
# Check if bot token is valid
curl -s "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```

#### AI Responses Not Working
- Verify `OPENAI_API_KEY` is set correctly
- Check OpenAI API quota and billing
- Monitor logs for API errors

#### Module Import Errors
```bash
# Reinstall dependencies
pip install --upgrade python-telegram-bot aiohttp python-dotenv openai
```

### Logging
The bot logs important events. Check console output for:
- ✅ Successful startup messages
- ⚠️ API warnings
- ❌ Error details

## 🔐 Security Best Practices

1. **Environment Variables**: Never commit `.env` files to version control
2. **API Keys**: Rotate OpenAI API keys regularly
3. **Bot Token**: Keep your Telegram bot token secure
4. **Rate Limiting**: Monitor API usage to prevent abuse
5. **User Data**: Conversation history is stored in memory only

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/telegram-agent-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/telegram-agent-bot/discussions)
- **Telegram**: [@yourusername](https://t.me/yourusername)

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Excellent Telegram Bot API wrapper
- [OpenAI](https://openai.com/) - AI capabilities powered by GPT
- [aiohttp](https://aiohttp.readthedocs.io/) - Async HTTP client for API requests

---

**Made with ❤️ for the Telegram community**

Ready to chat? Add your bot to Telegram and start the conversation! 🚀
