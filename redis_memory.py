"""Redis-based memory for storing user profiles and match history"""

import json
import redis
from typing import Dict, Any, List, Optional
from datetime import datetime


class RedisMemory:
    """Store and retrieve user profiles and match results using Redis"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            print(f"✓ Connected to Redis at {host}:{port}")
        except Exception as e:
            print(f"⚠ Redis connection failed: {e}")
            print("  Continuing without Redis memory...")
            self.redis_client = None
    
    def save_user_profile(self, username: str, profile: Dict[str, Any]) -> bool:
        """Save a user profile to Redis"""
        if not self.redis_client:
            return False
        
        try:
            key = f"user:{username}"
            profile['updated_at'] = datetime.now().isoformat()
            self.redis_client.set(key, json.dumps(profile))
            print(f"✓ Saved profile for {username}")
            return True
        except Exception as e:
            print(f"✗ Error saving profile: {e}")
            return False
    
    def get_user_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """Retrieve a user profile from Redis"""
        if not self.redis_client:
            return None
        
        try:
            key = f"user:{username}"
            data = self.redis_client.get(key)
            if data:
                profile = json.loads(data)
                print(f"✓ Retrieved profile for {username}")
                return profile
            return None
        except Exception as e:
            print(f"✗ Error retrieving profile: {e}")
            return None
    
    def save_match_result(self, username: str, matches: str, query: str = "") -> bool:
        """Save match results to Redis"""
        if not self.redis_client:
            return False
        
        try:
            key = f"matches:{username}"
            timestamp = datetime.now().isoformat()
            
            result = {
                "timestamp": timestamp,
                "query": query,
                "matches": matches
            }
            
            # Store in a list (keep match history)
            self.redis_client.rpush(key, json.dumps(result))
            
            # Set expiration to 30 days
            self.redis_client.expire(key, 30 * 24 * 60 * 60)
            
            print(f"✓ Saved match results for {username}")
            return True
        except Exception as e:
            print(f"✗ Error saving matches: {e}")
            return False
    
    def get_match_history(self, username: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get match history for a user"""
        if not self.redis_client:
            return []
        
        try:
            key = f"matches:{username}"
            data = self.redis_client.lrange(key, -limit, -1)
            
            if data:
                results = [json.loads(item) for item in data]
                print(f"✓ Retrieved {len(results)} match results for {username}")
                return results
            return []
        except Exception as e:
            print(f"✗ Error retrieving match history: {e}")
            return []
    
    def get_latest_match(self, username: str) -> Optional[Dict[str, Any]]:
        """Get the most recent match result for a user"""
        if not self.redis_client:
            return None
        
        try:
            key = f"matches:{username}"
            data = self.redis_client.lrange(key, -1, -1)
            
            if data:
                return json.loads(data[0])
            return None
        except Exception as e:
            print(f"✗ Error retrieving latest match: {e}")
            return None
    
    def update_user_preferences(self, username: str, updates: Dict[str, Any]) -> bool:
        """Update specific fields in a user's profile"""
        if not self.redis_client:
            return False
        
        try:
            profile = self.get_user_profile(username)
            if profile:
                profile.update(updates)
                return self.save_user_profile(username, profile)
            return False
        except Exception as e:
            print(f"✗ Error updating preferences: {e}")
            return False
    
    def list_all_users(self) -> List[str]:
        """List all users stored in Redis"""
        if not self.redis_client:
            return []
        
        try:
            keys = self.redis_client.keys("user:*")
            users = [key.replace("user:", "") for key in keys]
            return users
        except Exception as e:
            print(f"✗ Error listing users: {e}")
            return []
    
    def delete_user_profile(self, username: str) -> bool:
        """Delete a user profile and their match history"""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.delete(f"user:{username}")
            self.redis_client.delete(f"matches:{username}")
            print(f"✓ Deleted profile for {username}")
            return True
        except Exception as e:
            print(f"✗ Error deleting profile: {e}")
            return False
    
    def clear_all(self) -> bool:
        """Clear all user data (use with caution)"""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.flushdb()
            print("✓ Cleared all data from Redis")
            return True
        except Exception as e:
            print(f"✗ Error clearing data: {e}")
            return False
