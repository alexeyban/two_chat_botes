
# Telegram Bot Duo with DeepSeek AI

This project features two Telegram bots that engage in a continuous, AI-powered conversation with each other while also responding to user messages in a group chat. Powered by the DeepSeek API and built with Python, the bots alternate their dialogue every 10 seconds, creating a dynamic and interactive experience. All code was generated with assistance from Grok (xAI).

## Features
- **Continuous Bot Dialogue**: Bot1 and Bot2 chat endlessly, generating responses via DeepSeek AI.
- **User Interaction**: Both bots respond to user messages in the group using context-aware replies.
- **Modular Design**: Built step-by-step with AI assistance, showcasing task decomposition.

## Prerequisites
Before running the project, ensure the following are set up:

### Software Requirements
- **Python 3.10+**: Install from [python.org](https://www.python.org/downloads/).
- **pip**: Python package manager (usually included with Python).
- **Telegram Account**: Needed to create and manage bots.
- **DeepSeek API Key**: Sign up at [deepseek.com](https://deepseek.com) to obtain an API key.

### Python Libraries
Install the required libraries using pip:
```bash
pip install python-telegram-bot aiohttp
```

### Telegram Bot Setup
1. **Create Bots**:
   - Open Telegram and search for `@BotFather`.
   - Send `/newbot` and follow the prompts to create two bots:
     - Bot1: e.g., `@XXXXXXXXXXX1_bot`.
     - Bot2: e.g., `@XXXXXXXXXXX2_bot`.
   - Save the API tokens provided for each bot
   - 
2. **Add Bots to a Group**:
   - Create a Telegram group or use an existing one.
   - Add both bots to the group:
     - In the group, click the name → "Add Member" → search for each bot’s username → add them.
   - Grant admin privileges:
     - Group Settings → "Administrators" → add each bot → enable "Send Messages".

3. **Get Group CHAT_ID**:
   - Send a message in the group (e.g., "test").
   - Temporarily add this code to `bots.py` before `main()` to log the `CHAT_ID`:
     ```python
     async def get_chat_id(update, context):
         logger.info(f"CHAT_ID: {update.message.chat_id}")
     app1.add_handler(MessageHandler(filters.TEXT, get_chat_id))
     ```
   - Run the script, check the log for `CHAT_ID: -100XXXXXXXXXXX` (example), then update `CHAT_ID` in the code.

## Installation
1. **Clone or Download**:
   - Download this project or clone it via Git:
     ```bash
     git clone <repository-url>
     cd <repository-folder>
     ```

2. **Configure the Script**:
   - Open `bots.py` in a text editor.
   - Replace `DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY"` with your DeepSeek API key.
   - Update `TOKEN_BOT1` and `TOKEN_BOT2` with your bot tokens from BotFather.
   - Set `CHAT_ID` to your group’s ID (e.g., -100XXXXXXXXXXX`).

## Usage
1. **Run the Program**:
   - In the terminal, navigate to the project folder and execute:
     ```bash
     python bots.py
     ```
   - The bots will start their dialogue in the specified group.

2. **Interact with Bots**:
   - Open the Telegram group.
   - Watch Bot1 and Bot2 chat every 10 seconds.
   - Send a message (e.g., "Hey, bots!") to see them respond.

3. **Stop the Program**:
   - Press `Ctrl+C` in the terminal to halt the bots gracefully.

## How It Works
- **Bot Dialogue**: Bot1 starts with a greeting, Bot2 responds via DeepSeek, and they alternate with a 10-second delay.
- **User Response**: Messages from users trigger a DeepSeek-generated reply from the current bot, seamlessly resuming the bot-to-bot chat.
- **AI Assistance**: All code was crafted by Grok (xAI), demonstrating AI-driven development with minimal coding knowledge.

## Troubleshooting
- **Bots Don’t Respond**: Ensure tokens, `CHAT_ID`, and DeepSeek API key are correct; verify admin rights in the group.
- **Errors in Log**: Check for `TelegramError` or `DeepSeek API` issues—validate internet connection and API key.
- **Double Messages**: If a bot posts twice, restart the script and confirm the `turn` logic aligns.

## License
This project is open-source under the MIT License. Feel free to adapt and share!

## Acknowledgments
- Built with [Grok](https://grok.com) by xAI.
- Powered by [DeepSeek API](https://deepseek.com).
- Inspired by the power of AI to simplify complex coding tasks.
