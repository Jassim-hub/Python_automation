# Telegram Social Media Agent
# This agent posts to Telegram channels/groups using the free Telegram Bot API

import os
import json
import logging
import schedule
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import telebot  # Telegram API

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("telegram_agent.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

class TelegramAgent:
    def __init__(self):
        self.post_history = []
        self.load_data()
        
    def load_data(self):
        """Load existing post history"""
        try:
            if os.path.exists("telegram_history.json"):
                with open("telegram_history.json", "r") as f:
                    self.post_history = json.load(f)
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
    
    def save_data(self):
        """Save post history"""
        try:
            with open("telegram_history.json", "w") as f:
                json.dump(self.post_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
    
    def generate_content(self):
        """Generate day-specific content"""
        messages = [
            "Monday Motivation: Start your week with a positive mindset! 🚀",
            "Tuesday Tips: Consistency is key to success! 💡",
            "Wednesday Wisdom: Keep pushing forward! 💪",
            "Thursday Thoughts: Reflect and set new goals! 🎯",
            "Friday Fun: Almost weekend time! 🎉",
            "Saturday Vibes: Time to relax and recharge! 😌",
            "Sunday Reflections: Prepare for the week ahead! 📝",
        ]
        
        current_day = datetime.now().weekday()
        return messages[current_day]
    
    def post_to_telegram(self, content):
        """Post to Telegram channel (Free)"""
        try:
            bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            chat_id = os.getenv("TELEGRAM_CHAT_ID")
            
            if not bot_token or not chat_id:
                logger.error("Telegram credentials not found in .env file")
                return False
            
            bot = telebot.TeleBot(bot_token)
            bot.send_message(chat_id, content)
            
            logger.info(f"Posted to Telegram: {content[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Telegram posting failed: {str(e)}")
            return False
    
    def post_daily_content(self):
        """Post day-specific content to Telegram"""
        content = self.generate_content()
        
        success = self.post_to_telegram(content)
        
        # Save to history
        post_data = {
            "content": content,
            "date": str(datetime.now().date()),
            "time": datetime.now().strftime("%H:%M:%S"),
            "success": success
        }
        
        self.post_history.append(post_data)
        self.save_data()
        
        if success:
            logger.info("Successfully posted to Telegram")
        else:
            logger.error("Failed to post to Telegram")
        
        return success
    
    def get_post_stats(self):
        """Get statistics about posts"""
        if not self.post_history:
            return {"total_posts": 0, "successful_posts": 0, "success_rate": 0}
        
        total_posts = len(self.post_history)
        successful_posts = sum(1 for post in self.post_history if post.get("success", False))
        success_rate = (successful_posts / total_posts) * 100 if total_posts > 0 else 0
        
        return {
            "total_posts": total_posts,
            "successful_posts": successful_posts,
            "success_rate": round(success_rate, 2)
        }

# Interactive menu
def main():
    agent = TelegramAgent()
    
    print("🤖 Telegram Social Media Agent")
    print("=" * 40)
    
    while True:
        print("\nChoose an option:")
        print("1. Test Telegram posting")
        print("2. Post today's content")
        print("3. Start automated posting")
        print("4. View post history")
        print("5. View post statistics")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            content = input("Enter message for Telegram: ")
            if agent.post_to_telegram(content):
                print("✅ Telegram post successful!")
            else:
                print("❌ Telegram post failed!")
        
        elif choice == "2":
            if agent.post_daily_content():
                print("✅ Daily content posted successfully!")
            else:
                print("❌ Failed to post daily content!")
        
        elif choice == "3":
            print("🚀 Starting automated posting...")
            schedule.every().day.at("09:00").do(agent.post_daily_content)
            schedule.every().day.at("18:00").do(agent.post_daily_content)
            
            print("Automated posting scheduled for 9:00 AM and 6:00 PM daily")
            print("Press Ctrl+C to stop")
            
            try:
                while True:
                    schedule.run_pending()
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\n👋 Automated posting stopped!")
        
        elif choice == "4":
            if agent.post_history:
                print("\n📊 Post History (Last 10 posts):")
                for i, post in enumerate(agent.post_history[-10:], 1):
                    status = "✅" if post.get("success", False) else "❌"
                    print(f"{i}. {post['date']} {post['time']} {status} - {post['content'][:50]}...")
            else:
                print("No post history available")
        
        elif choice == "5":
            stats = agent.get_post_stats()
            print(f"\n📈 Post Statistics:")
            print(f"Total posts: {stats['total_posts']}")
            print(f"Successful posts: {stats['successful_posts']}")
            print(f"Success rate: {stats['success_rate']}%")
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
