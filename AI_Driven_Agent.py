# Post Automation Agent
# Create an AI-driven agent that automates tasks of creating posts on X.com (formerly Twitter) using Python.
# for a period of 30 days, with a focus on automating the process of posting content, engaging with followers, and
# analyzing post performance.

# How it will work:
# 1. **Content Creation**: The agent will generate content ideas based on trending topics and user interests.
# 2. **Post Scheduling**: It will schedule posts at optimal times for maximum engagement.
# 3. **Engagement**: The agent will respond to comments and messages, fostering community interaction.
# 4. **Performance Analysis**: It will analyze post performance and adjust strategies accordingly.
# 5. **Learning and Adaptation**: The agent will learn from user interactions and adapt its strategies over time.

# Import necessary libraries
import tweepy
import schedule
import time
import random
from datetime import datetime, timedelta
import logging
import json
import os
from dotenv import load_dotenv  # This imports my environment variables

# Load environment variables
load_dotenv()

# X.com API credentials (secure method)
API_KEY = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Authenticate to the X.com API
auth = tweepy.OAuth1UserHandler(API_KEY, api_secret, ACCESS_TOKEN, access_token_secret)
api = tweepy.API(auth)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("twitter_agent.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Predefine list of daily message posts
messages = [
    "Monday Motivation: Start your week with a positive mindset! #MondayMotivation",
    "Tuesday Tips: Did you know that consistency is key to success? #TuesdayTips",
    "Wednesday Wisdom: Keep pushing forward, you're halfway through the week! #WednesdayWisdom",
    "Thursday Thoughts: Reflect on your progress and set new goals! #ThursdayThoughts",
    "Friday Fun: It's almost the weekend! What are your plans? #FridayFun",
    "Saturday Vibes: Take a break and enjoy some leisure time! #SaturdayVibes",
    "Sunday Reflections: Prepare for the week ahead and set your intentions! #SundayReflections",
]

# Additional content for variety
tech_content = [
    "🚀 The future of AI is here! What's your favorite AI tool? #AI #Technology",
    "💡 Automation tip: Small repetitive tasks can save hours when automated! #Automation",
    "🔧 Python tip: Use list comprehensions for cleaner, faster code! #Python #Programming",
    "📊 Data is the new oil, but insights are the refined fuel! #DataScience",
    "🤖 Building the future, one line of code at a time! #Coding #Innovation",
]

# Initialize data storage
post_history = []
analytics_data = []

# Configuration
MAX_POSTS_PER_DAY = 5
POSTING_TIMES = ["09:00", "12:00", "15:00", "18:00", "21:00"]


# Step 1: Content Creation Function
def generate_content():
    """Generate content based on current day and add variety"""
    current_day = datetime.now().weekday()  # 0=Monday, 6=Sunday

    # Map weekday numbers to message indices
    day_names = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # Log  day we posting 4
    logger.info(f"Generating content for {day_names[current_day]}")

    # Choose content based on day
    if current_day < len(messages):
        base_content = messages[current_day]
    else:
        base_content = random.choice(messages)

    # Add tech content occasionally
    if random.random() < 0.3:  # 30% chance for tech content
        tech_post = random.choice(tech_content)
        logger.info(f"Using tech content instead of {day_names[current_day]} content")
        return tech_post

    logger.info(f"Using {day_names[current_day]} content: {base_content[:30]}...")
    return base_content


# Step 2: Post Scheduling Function
def create_post():
    """Create and post a tweet"""
    try:
        # Check if we've reached daily limit
        today = datetime.now().date()
        today_posts = [p for p in post_history if p["date"] == str(today)]

        if len(today_posts) >= MAX_POSTS_PER_DAY:
            logger.warning("Daily posting limit reached")
            return

        # Generate content
        content = generate_content()

        # Post the tweet
        tweet = api.update_status(content)

        # Save to history
        post_data = {
            "id": str(tweet.id),
            "content": content,
            "date": str(today),
            "time": datetime.now().strftime("%H:%M:%S"),
            "likes": 0,
            "retweets": 0,
            "replies": 0,
        }

        post_history.append(post_data)
        save_data()

        logger.info(f"Tweet posted: {content[:50]}...")

    except Exception as e:
        logger.error(f"Error posting tweet: {str(e)}")


# Step 3: Engagement Function
def engage_with_followers():
    """Engage with mentions and followers"""
    try:
        # Get mentions
        mentions = api.mentions_timeline(count=5)

        for mention in mentions:
            # Simple engagement responses
            responses = [
                "Thank you for the mention! 🙏",
                "Appreciate your engagement! 💪",
                "Thanks for connecting! 🤝",
                "Great to hear from you! 😊",
            ]

            # Reply to mention
            response = random.choice(responses)
            api.update_status(
                f"@{mention.user.screen_name} {response}",
                in_reply_to_status_id=mention.id,
            )

            logger.info(f"Replied to @{mention.user.screen_name}")

    except Exception as e:
        logger.error(f"Error engaging with followers: {str(e)}")


# Step 4: Performance Analysis Function
def analyze_performance():
    """Analyze post performance and gather metrics"""
    try:
        # Update metrics for recent posts
        for post in post_history[-10:]:  # Last 10 posts
            try:
                tweet = api.get_status(post["id"])
                post["likes"] = tweet.favorite_count
                post["retweets"] = tweet.retweet_count

                # Calculate engagement
                engagement = post["likes"] + post["retweets"]
                post["engagement"] = engagement

            except Exception as e:
                logger.error(f"Error analyzing tweet {post['id']}: {str(e)}")
                continue

        # Generate analytics report
        if post_history:
            total_posts = len(post_history)
            total_likes = sum(p.get("likes", 0) for p in post_history)
            total_retweets = sum(p.get("retweets", 0) for p in post_history)
            avg_engagement = (
                (total_likes + total_retweets) / total_posts if total_posts > 0 else 0
            )

            analytics_report = {
                "date": str(datetime.now().date()),
                "total_posts": total_posts,
                "total_likes": total_likes,
                "total_retweets": total_retweets,
                "average_engagement": avg_engagement,
            }

            analytics_data.append(analytics_report)
            save_data()

            logger.info(
                f"Analytics: {total_posts} posts, {avg_engagement:.2f} avg engagement"
            )

    except Exception as e:
        logger.error(f"Error analyzing performance: {str(e)}")


# Step 5: Learning and Adaptation Function
def adapt_strategy():
    """Adapt posting strategy based on performance"""
    try:
        if len(post_history) < 5:
            return

        # Find best performing posts
        best_posts = sorted(
            post_history, key=lambda x: x.get("engagement", 0), reverse=True
        )[:3]

        # Log insights
        logger.info("Top performing content types:")
        for i, post in enumerate(best_posts[:3], 1):
            logger.info(
                f"{i}. {post['content'][:30]}... (Engagement: {post.get('engagement', 0)})"
            )

        # Adapt content based on performance
        if best_posts:
            best_content = best_posts[0]["content"]
            if "#AI" in best_content or "#Technology" in best_content:
                # Increase tech content probability
                logger.info("Adapting: Increasing tech content based on performance")

    except Exception as e:
        logger.error(f"Error adapting strategy: {str(e)}")


# Data Management Functions
def save_data():
    """Save post history and analytics data"""
    try:
        with open("post_history.json", "w") as f:
            json.dump(post_history, f, indent=2)

        with open("analytics_data.json", "w") as f:
            json.dump(analytics_data, f, indent=2)

    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")


def load_data():
    """Load existing data"""
    global post_history, analytics_data

    try:
        if os.path.exists("post_history.json"):
            with open("post_history.json", "r") as f:
                post_history = json.load(f)

        if os.path.exists("analytics_data.json"):
            with open("analytics_data.json", "r") as f:
                analytics_data = json.load(f)

    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")


# Scheduling Functions
def schedule_posts():
    """Schedule posts at optimal times"""
    for time_slot in POSTING_TIMES:
        schedule.every().day.at(time_slot).do(create_post)

    # Schedule engagement activities
    schedule.every(2).hours.do(engage_with_followers)

    # Schedule daily analytics
    schedule.every().day.at("23:00").do(analyze_performance)

    # Schedule weekly strategy adaptation
    schedule.every().monday.at("08:00").do(adapt_strategy)

    logger.info("All tasks scheduled successfully!")


# Main execution function
def run_agent(days=30):
    """Run the AI agent for specified number of days"""
    logger.info(f"Starting AI Twitter Agent for {days} days...")

    # Load existing data
    load_data()

    # Verify API connection
    try:
        api.verify_credentials()
        logger.info("API authentication successful!")
    except Exception as e:
        logger.error(f"API authentication failed: {str(e)}")
        return

    # Schedule all tasks
    schedule_posts()

    # Run the agent
    end_date = datetime.now() + timedelta(days=days)

    while datetime.now() < end_date:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

        except KeyboardInterrupt:
            logger.info("Agent stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            time.sleep(300)  # Wait 5 minutes before retrying

    logger.info("AI Twitter Agent completed successfully!")


# Testing and Manual Functions
def test_post():
    """Test posting functionality"""
    try:
        content = "🤖 Testing my AI Twitter Agent! This is automated content creation in action. #AI #Automation #Test"
        tweet = api.update_status(content)
        logger.info(f"Test tweet posted successfully: {tweet.id}")
        return True
    except Exception as e:
        logger.error(f"Test post failed: {str(e)}")
        return False


def manual_post(content):
    """Manually post custom content"""
    try:
        tweet = api.update_status(content)
        logger.info(f"Manual tweet posted: {content[:50]}...")
        return True
    except Exception as e:
        logger.error(f"Manual post failed: {str(e)}")
        return False


def get_analytics_summary():
    """Get current analytics summary"""
    if not analytics_data:
        return "No analytics data available yet."

    latest = analytics_data[-1]
    return f"""
    📊 Latest Analytics Summary:
    📅 Date: {latest['date']}
    📝 Total Posts: {latest['total_posts']}
    ❤️ Total Likes: {latest['total_likes']}
    🔄 Total Retweets: {latest['total_retweets']}
    📈 Average Engagement: {latest['average_engagement']:.2f}
    """


# Interactive Menu
def main():
    """Main function with interactive menu"""
    print("🤖 AI Twitter Agent - Interactive Menu")
    print("=" * 40)

    while True:
        print("\nChoose an option:")
        print("1. Test API connection")
        print("2. Post a test tweet")
        print("3. Post custom content")
        print("4. Start 30-day automation")
        print("5. Check analytics")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == "1":
            try:
                api.verify_credentials()
                print("✅ API connection successful!")
            except Exception as e:
                print(f"❌ API connection failed: {str(e)}")

        elif choice == "2":
            if test_post():
                print("✅ Test tweet posted successfully!")
            else:
                print("❌ Test tweet failed!")

        elif choice == "3":
            content = input("Enter your tweet content: ")
            if manual_post(content):
                print("✅ Tweet posted successfully!")
            else:
                print("❌ Tweet posting failed!")

        elif choice == "4":
            print("🚀 Starting 30-day automation...")
            run_agent(30)

        elif choice == "5":
            print(get_analytics_summary())

        elif choice == "6":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")


# Graded Assignment (20): Create an AI agent that automates tasks of creating posts on social media platforms
# like X.com (formerly Twitter), LinkedIn, Pinterest, Telegram (etc) using Python.

if __name__ == "__main__":
    main()
