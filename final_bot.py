
#!/usr/bin/env python3
"""AI-Powered Telegram Agent Bot - Fixed Version"""

import os
import logging
import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional, List
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProcessor:
    """Handles AI language model interactions for natural conversation"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.enabled = bool(self.api_key)
        self.conversation_history = {}  # Store conversation context per user
        
    async def analyze_intent(self, message: str) -> Dict[str, Any]:
        """Analyze user message intent and sentiment"""
        if not self.enabled:
            return self._fallback_analysis(message)
        
        try:
            timeout = aiohttp.ClientTimeout(total=10)  # Add timeout
            async with aiohttp.ClientSession(timeout=timeout) as session:
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [{
                        "role": "user", 
                        "content": f'Analyze this message and return JSON with intent classification: "{message}"\n\nReturn: {{"intent": "question|request|greeting|chitchat|help", "sentiment": "positive|neutral|negative", "topic": "general|technical|personal|other"}}'
                    }],
                    "max_tokens": 100,
                    "temperature": 0.1
                }
                headers = {
                    "Authorization": f"Bearer {self.api_key}", 
                    "Content-Type": "application/json"
                }
                
                async with session.post("https://api.openai.com/v1/chat/completions", 
                                       headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result['choices'][0]['message']['content'].strip()
                        content = content.replace("```json", "").replace("```", "").strip()
                        return json.loads(content)
                    else:
                        logger.warning(f"OpenAI API error: {response.status}")
        except asyncio.TimeoutError:
            logger.warning("LLM analysis timed out")
        except json.JSONDecodeError as e:
            logger.warning(f"JSON decode error in LLM analysis: {e}")
        except Exception as e:
            logger.warning(f"LLM analysis failed: {e}")
        
        return self._fallback_analysis(message)
    
    def _fallback_analysis(self, message: str) -> Dict[str, Any]:
        """Simple keyword-based analysis when LLM is unavailable"""
        m = message.lower()
        
        # Intent detection
        if any(word in m for word in ["hello", "hi", "hey", "good morning", "good evening"]):
            intent = "greeting"
        elif any(word in m for word in ["help", "how to", "what is", "explain"]):
            intent = "help"
        elif any(word in m for word in ["please", "can you", "could you", "would you"]):
            intent = "request"
        elif "?" in message:
            intent = "question"
        else:
            intent = "chitchat"
        
        # Sentiment detection
        if any(word in m for word in ["great", "good", "excellent", "love", "amazing", "happy"]):
            sentiment = "positive"
        elif any(word in m for word in ["bad", "terrible", "awful", "hate", "angry", "frustrated"]):
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "intent": intent,
            "sentiment": sentiment,
            "topic": "general"
        }
    
    async def generate_response(self, user_id: str, message: str, context: str = "") -> str:
        """Generate contextual response using LLM"""
        if not self.enabled:
            return self._fallback_response(message)
        
        # Get conversation history
        history = self.conversation_history.get(user_id, [])
        
        try:
            timeout = aiohttp.ClientTimeout(total=15)  # Add timeout
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Build conversation context
                messages = [
                    {"role": "system", "content": "You are a helpful AI assistant in a Telegram bot. Be friendly, concise, and helpful. Keep responses under 200 words unless specifically asked for more detail."}
                ]
                
                # Add recent conversation history (last 5 exchanges)
                for hist in history[-5:]:
                    messages.append({"role": "user", "content": hist["user"]})
                    messages.append({"role": "assistant", "content": hist["bot"]})
                
                # Add current message
                if context:
                    messages.append({"role": "user", "content": f"Context: {context}\nUser message: {message}"})
                else:
                    messages.append({"role": "user", "content": message})
                
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": messages,
                    "max_tokens": 300,
                    "temperature": 0.7
                }
                headers = {
                    "Authorization": f"Bearer {self.api_key}", 
                    "Content-Type": "application/json"
                }
                
                async with session.post("https://api.openai.com/v1/chat/completions", 
                                       headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        bot_response = result['choices'][0]['message']['content'].strip()
                        
                        # Update conversation history
                        self._update_history(user_id, message, bot_response)
                        return bot_response
                    else:
                        logger.warning(f"OpenAI API error: {response.status} - {await response.text()}")
        except asyncio.TimeoutError:
            logger.warning("LLM response generation timed out")
        except Exception as e:
            logger.warning(f"LLM response generation failed: {e}")
        
        return self._fallback_response(message)
    
    def _update_history(self, user_id: str, user_message: str, bot_response: str):
        """Update conversation history for context"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            "user": user_message,
            "bot": bot_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 10 exchanges to manage memory
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
    
    def _fallback_response(self, message: str) -> str:
        """Simple fallback responses when LLM is unavailable"""
        m = message.lower()
        
        # More intelligent fallback responses based on keywords
        if any(word in m for word in ["hello", "hi", "hey"]):
            return "Hello! Nice to meet you. How can I help you today?"
        elif any(word in m for word in ["thanks", "thank you"]):
            return "You're welcome! Is there anything else I can help you with?"
        elif any(word in m for word in ["bye", "goodbye", "see you"]):
            return "Goodbye! Feel free to message me anytime you need help."
        elif "?" in message:
            return "That's a great question! I'm here to help, though my AI features might be limited right now."
        else:
            responses = [
                "I understand. How can I help you with that?",
                "That's interesting! Tell me more.",
                "I'm here to help. What would you like to know?",
                "Thanks for sharing that with me.",
                "I see. Is there anything specific you'd like assistance with?"
            ]
            return responses[hash(message) % len(responses)]
    
    def clear_history(self, user_id: str):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]

class TelegramAgentBot:
    """Main Telegram bot class with AI agent capabilities"""
    
    def __init__(self, telegram_token: str):
        # Build application with better error handling
        try:
            self.app = Application.builder().token(telegram_token).build()
        except Exception as e:
            logger.error(f"Failed to initialize Telegram Application: {e}")
            raise
            
        self.llm = LLMProcessor()
        self.user_sessions = {}  # Track user sessions
        
        # Register command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("clear", self.clear_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        
        # Register message handler for natural conversation
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info(f"Bot initialized with LLM: {'✅ Enabled' if self.llm.enabled else '❌ Disabled'}")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_name = update.effective_user.first_name or "there"
        welcome_message = f"""🤖 **AI Agent Bot**

Hello {user_name}! I'm your AI assistant. I can help you with:

✨ **Natural Conversation** - Just talk to me!
🤔 **Questions & Answers** - Ask me anything
🛠️ **General Assistance** - I'm here to help

Just send me a message and I'll respond naturally.

Type /help for more commands."""

        await update.message.reply_text(welcome_message, parse_mode='Markdown')
        
        # Initialize user session
        user_id = str(update.effective_user.id)
        self.user_sessions[user_id] = {
            "started_at": datetime.now(),
            "message_count": 0,
            "name": update.effective_user.full_name
        }
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """🆘 **Available Commands:**

🤖 **Natural Chat** - Just type any message!
• Ask questions, request help, or chat casually
• I'll understand context from our conversation

📝 **Commands:**
• `/start` - Initialize the bot
• `/help` - Show this help message  
• `/clear` - Clear conversation history
• `/status` - Show your session info

💡 **Examples:**
• "What's the weather like?"
• "Help me write an email"
• "Tell me a joke"
• "Explain quantum physics simply"

Just type naturally - I'm designed to understand and help! 🚀"""

        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /clear command to reset conversation history"""
        user_id = str(update.effective_user.id)
        self.llm.clear_history(user_id)
        
        await update.message.reply_text(
            "🧹 **Conversation history cleared!**\n\n"
            "I've forgotten our previous conversation. We can start fresh! 🆕",
            parse_mode='Markdown'
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command to show user session info"""
        user_id = str(update.effective_user.id)
        session = self.user_sessions.get(user_id, {})
        
        if not session:
            await update.message.reply_text("❓ No active session. Use /start to begin!")
            return
        
        started_at = session.get("started_at", datetime.now())
        duration = datetime.now() - started_at
        hours, remainder = divmod(int(duration.total_seconds()), 3600)
        minutes, _ = divmod(remainder, 60)
        
        history_count = len(self.llm.conversation_history.get(user_id, []))
        
        status_text = f"""📊 **Your Session Status**

👤 **User:** {session.get('name', 'Unknown')}
🕒 **Session Duration:** {hours}h {minutes}m
💬 **Messages Exchanged:** {session.get('message_count', 0)}
🧠 **Conversation Memory:** {history_count} exchanges
🤖 **AI Status:** {'🟢 Active' if self.llm.enabled else '🔴 Offline'}

Ready to chat! 🚀"""

        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages with AI processing"""
        try:
            user_id = str(update.effective_user.id)
            user_message = update.message.text
            
            # Update user session
            if user_id in self.user_sessions:
                self.user_sessions[user_id]["message_count"] += 1
            else:
                # Auto-initialize session if not started
                self.user_sessions[user_id] = {
                    "started_at": datetime.now(),
                    "message_count": 1,
                    "name": update.effective_user.full_name or "User"
                }
            
            # Show typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Analyze message intent
            analysis = await self.llm.analyze_intent(user_message)
            
            # Generate contextual response
            response = await self.llm.generate_response(
                user_id, 
                user_message, 
                context=f"Intent: {analysis.get('intent', 'unknown')}, Sentiment: {analysis.get('sentiment', 'neutral')}"
            )
            
            # Send response
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "😅 Sorry, I encountered an issue processing your message. "
                "Please try again or use /help for available commands."
            )
    
    def run(self):
        """Start the bot with improved error handling"""
        logger.info("🚀 Starting Telegram Agent Bot...")
        
        try:
            # Use asyncio to run the bot
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Start polling with error handling
            self.app.run_polling(
                drop_pending_updates=True,
                close_loop=False,
                stop_signals=None  # Disable signal handling to avoid conflicts
            )
            
        except KeyboardInterrupt:
            logger.info("👋 Bot stopped by user")
        except Exception as e:
            logger.error(f"Bot error: {e}")
            # Print more detailed error information
            import traceback
            logger.error(f"Detailed error: {traceback.format_exc()}")
            raise

def main():
    """Main entry point with enhanced error handling"""
    # Check for required token
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("❌ Missing TELEGRAM_BOT_TOKEN environment variable!")
        print("Please set TELEGRAM_BOT_TOKEN in your .env file or environment variables.")
        return 1
    
    # Validate token format
    if not token.startswith(('bot', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
        logger.error("❌ Invalid TELEGRAM_BOT_TOKEN format!")
        print("Token should start with bot prefix or be numeric.")
        return 1
    
    # Optional: Check for OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        logger.warning("⚠️ No OPENAI_API_KEY found. Bot will work with basic responses.")
        print("Tip: Set OPENAI_API_KEY for enhanced AI responses.")
    
    try:
        # Test token validity first
        logger.info("🔍 Validating Telegram bot token...")
        
        bot = TelegramAgentBot(token)
        bot.run()
        return 0
        
    except Exception as e:
        logger.error(f"💥 Failed to start bot: {e}")
        print(f"\nDetailed error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your TELEGRAM_BOT_TOKEN is correct")
        print("2. Ensure you have internet connectivity")
        print("3. Try: pip install --upgrade python-telegram-bot httpx aiohttp")
        print("4. Or pin versions: pip install python-telegram-bot==20.7 httpx==0.24.1")
        return 1

if __name__ == "__main__":
    exit(main())
