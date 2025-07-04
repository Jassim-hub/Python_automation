#!/usr/bin/env python3
"""
Twitter API Test Script
Tests what your Twitter API credentials can actually do with the free tier.
"""

import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_twitter_credentials():
    """Test Twitter API credentials and available functions"""
    print("🔍 Testing Twitter API Credentials...")
    
    # Load credentials from .env file
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("❌ Missing credentials in .env file")
        return False
    
    try:
        # Initialize API v1.1 (older version)
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        
        # Test 1: Verify credentials
        print("\n📋 Test 1: Verifying credentials...")
        try:
            user = api.verify_credentials()
            print(f"✅ Credentials verified! Logged in as: @{user.screen_name}")
            print(f"   Account created: {user.created_at}")
            print(f"   Followers: {user.followers_count}")
            print(f"   Following: {user.friends_count}")
            print(f"   Tweets: {user.statuses_count}")
        except Exception as e:
            print(f"❌ Credential verification failed: {e}")
            return False
        
        # Test 2: Try to get user timeline (read-only)
        print("\n📋 Test 2: Reading user timeline...")
        try:
            tweets = api.user_timeline(count=1)
            if tweets:
                print(f"✅ Can read timeline! Latest tweet: {tweets[0].text[:100]}...")
            else:
                print("✅ Can read timeline (but no tweets found)")
        except Exception as e:
            print(f"❌ Timeline read failed: {e}")
        
        # Test 3: Try to get followers (read-only)
        print("\n📋 Test 3: Reading followers...")
        try:
            followers = api.get_followers(count=1)
            print(f"✅ Can read followers! Found {len(followers)} followers in sample")
        except Exception as e:
            print(f"❌ Followers read failed: {e}")
        
        # Test 4: Try to post a tweet (THIS WILL FAIL on free tier)
        print("\n📋 Test 4: Attempting to post a test tweet...")
        try:
            test_tweet = "🤖 Testing Twitter API access - this is a test tweet from my AI agent"
            result = api.update_status(test_tweet)
            print(f"✅ Tweet posted successfully! Tweet ID: {result.id}")
        except Exception as e:
            print(f"❌ Tweet posting failed: {e}")
            print("   This is expected on Twitter's free tier - posting requires paid plan")
        
        # Test 5: Try to get mentions (read-only)
        print("\n📋 Test 5: Reading mentions...")
        try:
            mentions = api.mentions_timeline(count=1)
            print(f"✅ Can read mentions! Found {len(mentions)} mentions in sample")
        except Exception as e:
            print(f"❌ Mentions read failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ General API error: {e}")
        return False

def test_twitter_v2_api():
    """Test Twitter API v2 (newer version)"""
    print("\n🔍 Testing Twitter API v2...")
    
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    if not bearer_token:
        print("❌ No bearer token found for v2 API")
        return False
    
    try:
        # Initialize API v2
        client = tweepy.Client(bearer_token=bearer_token)
        
        # Test: Get user info
        print("\n📋 Test: Getting user info with v2 API...")
        try:
            user = client.get_me()
            print(f"✅ v2 API working! User: @{user.data.username}")
        except Exception as e:
            print(f"❌ v2 API failed: {e}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ v2 API general error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Twitter API Testing Tool")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file with your Twitter API credentials:")
        print("""
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
""")
        exit(1)
    
    # Test v1.1 API
    success_v1 = test_twitter_credentials()
    
    # Test v2 API
    success_v2 = test_twitter_v2_api()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"Twitter API v1.1: {'✅ Working' if success_v1 else '❌ Failed'}")
    print(f"Twitter API v2: {'✅ Working' if success_v2 else '❌ Failed'}")
    print("\n💡 RECOMMENDATION:")
    if success_v1:
        print("✅ Your credentials work for READ-ONLY operations")
        print("❌ Posting tweets requires Twitter Basic plan ($100/month)")
        print("💡 Consider using the alternative platforms agent for free posting")
    else:
        print("❌ Credential issues detected - check your .env file")
