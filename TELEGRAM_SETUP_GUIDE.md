# Telegram Social Media Agent Setup Guide

## Overview
This Telegram agent posts day-specific motivational content to your Telegram channel, group, or personal chat using the free Telegram Bot API.

## Features
- ✅ Day-specific content posting (Monday Motivation, Tuesday Tips, etc.)
- ✅ Automated scheduling (9 AM and 6 PM daily)
- ✅ Post history tracking
- ✅ Success rate statistics
- ✅ Interactive menu for testing and management
- ✅ Completely FREE (no API costs)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements_telegram.txt
```

### 2. Create a Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Get Your Chat ID
**For Personal Chat:**
1. Send a message to your bot
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for "chat":{"id": YOUR_CHAT_ID}

**For Channel:**
1. Add your bot to the channel as an admin
2. Use the channel username with @ (e.g., `@your_channel`)

**For Group:**
1. Add your bot to the group
2. Send `/my_id` to @userinfobot in the group to get the group ID

### 4. Configure Environment Variables
1. Copy `.env_telegram_template` to `.env`
2. Fill in your credentials:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token
TELEGRAM_CHAT_ID=your_actual_chat_id
```

### 5. Run the Agent
```bash
python telegram_agent.py
```

## Usage Options

### Interactive Menu
- **Option 1**: Test posting with custom message
- **Option 2**: Post today's motivational content
- **Option 3**: Start automated posting (9 AM & 6 PM daily)
- **Option 4**: View post history
- **Option 5**: View success statistics
- **Option 6**: Exit

### Automated Posting
The agent will automatically post:
- Monday: "Monday Motivation: Start your week with a positive mindset! 🚀"
- Tuesday: "Tuesday Tips: Consistency is key to success! 💡"
- Wednesday: "Wednesday Wisdom: Keep pushing forward! 💪"
- Thursday: "Thursday Thoughts: Reflect and set new goals! 🎯"
- Friday: "Friday Fun: Almost weekend time! 🎉"
- Saturday: "Saturday Vibes: Time to relax and recharge! 😌"
- Sunday: "Sunday Reflections: Prepare for the week ahead! 📝"

## Files Created
- `telegram_history.json`: Post history data
- `telegram_agent.log`: Detailed logging

## Troubleshooting

### Common Issues
1. **"Telegram credentials not found"**
   - Check your `.env` file exists and has correct values
   - Ensure no extra spaces in the values

2. **"Chat not found"**
   - Verify the chat ID is correct
   - For channels, make sure bot is admin
   - For groups, ensure bot is added as member

3. **"Unauthorized"**
   - Check your bot token is correct
   - Ensure you copied the full token from BotFather

### Testing Your Setup
1. Run the agent
2. Choose option 1 (Test Telegram posting)
3. Enter a test message
4. Check if the message appears in your chat/channel

## Security Notes
- Never share your bot token publicly
- Keep your `.env` file secure and don't commit it to version control
- The bot token gives full access to your bot

## Customization
You can easily modify the daily messages in the `generate_content()` method of the `TelegramAgent` class.
