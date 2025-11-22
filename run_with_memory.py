#!/usr/bin/env python3
"""Interactive Hackathon Matching Agent with Redis Memory"""

import json
from agent_new import HackathonMatchingAgent
from redis_memory import RedisMemory


def display_menu():
    """Display main menu"""
    print("\n" + "=" * 60)
    print("🎯 HACKATHON TEAM MATCHING AGENT (with Redis Memory)")
    print("=" * 60)
    print("\n1. Create/Update Profile & Find Matches")
    print("2. View Your Profile")
    print("3. View Match History")
    print("4. Update Profile Preferences")
    print("5. View All Saved Users")
    print("6. Delete Profile")
    print("7. Exit")
    return input("\nChoose an option (1-7): ").strip()


def get_or_create_profile(memory: RedisMemory, username: str) -> dict:
    """Get existing profile or create new one"""
    profile = memory.get_user_profile(username)
    
    if profile:
        print(f"\n✓ Found existing profile for {username}")
        print("Do you want to:")
        print("  1. Use current profile")
        print("  2. Update profile")
        choice = input("  Choose (1-2): ").strip()
        
        if choice == "2":
            profile = update_profile(profile)
        return profile
    else:
        print(f"\n📝 Creating new profile for {username}")
        return create_profile()


def create_profile() -> dict:
    """Create a new user profile"""
    profile = {
        "name": input("Your name: ").strip(),
        "skills": [s.strip() for s in input("Your skills (comma-separated): ").strip().split(",")],
        "interests": [i.strip() for i in input("Your interests (comma-separated): ").strip().split(",")],
        "experience_level": input("Experience level (beginner/intermediate/advanced): ").strip(),
        "role_preferences": [r.strip() for r in input("Role preferences (comma-separated): ").strip().split(",")],
        "preferences": input("What are you looking for in a team? ").strip()
    }
    return profile


def update_profile(profile: dict) -> dict:
    """Update existing profile"""
    print("\nWhat would you like to update?")
    print("  1. Skills")
    print("  2. Interests")
    print("  3. Experience level")
    print("  4. Role preferences")
    print("  5. Team preferences")
    print("  6. Cancel")
    
    choice = input("Choose (1-6): ").strip()
    
    if choice == "1":
        profile["skills"] = [s.strip() for s in input("New skills (comma-separated): ").strip().split(",")]
    elif choice == "2":
        profile["interests"] = [i.strip() for i in input("New interests (comma-separated): ").strip().split(",")]
    elif choice == "3":
        profile["experience_level"] = input("New experience level: ").strip()
    elif choice == "4":
        profile["role_preferences"] = [r.strip() for r in input("New role preferences (comma-separated): ").strip().split(",")]
    elif choice == "5":
        profile["preferences"] = input("New team preferences: ").strip()
    
    return profile


def main():
    """Main application loop"""
    print("\n" + "=" * 60)
    print("🚀 Hackathon Matching Agent - Redis Memory Edition")
    print("=" * 60)
    
    username = input("\nEnter your username (e.g., 'guna'): ").strip().lower()
    
    # Initialize Redis memory and agent
    memory = RedisMemory()
    agent = HackathonMatchingAgent()
    
    while True:
        choice = display_menu()
        
        if choice == "1":
            # Create/Update profile and find matches
            print("\n" + "-" * 60)
            profile = get_or_create_profile(memory, username)
            
            # Save profile to Redis
            memory.save_user_profile(username, profile)
            
            print(f"\n🔍 Finding matches for {profile['name']}...")
            print("-" * 60)
            
            result = agent.match_person(profile)
            
            print("\n✅ Match Results:\n")
            print(result["matches"])
            
            # Save results to Redis
            memory.save_match_result(
                username,
                result["matches"],
                f"Skills: {', '.join(profile['skills'])}, Interests: {', '.join(profile['interests'])}"
            )
            
            print("\n💾 Results saved to Redis memory")
        
        elif choice == "2":
            # View current profile
            profile = memory.get_user_profile(username)
            
            if profile:
                print("\n" + "=" * 60)
                print(f"Profile for: {profile['name']}")
                print("=" * 60)
                print(f"Skills: {', '.join(profile['skills'])}")
                print(f"Interests: {', '.join(profile['interests'])}")
                print(f"Experience Level: {profile['experience_level']}")
                print(f"Role Preferences: {', '.join(profile['role_preferences'])}")
                print(f"Looking For: {profile['preferences']}")
                print(f"Last Updated: {profile.get('updated_at', 'N/A')}")
            else:
                print("\n⚠ No profile found. Create one first (Option 1)")
        
        elif choice == "3":
            # View match history
            history = memory.get_match_history(username, limit=10)
            
            if history:
                print("\n" + "=" * 60)
                print(f"Match History for {username}")
                print("=" * 60)
                
                for i, item in enumerate(history, 1):
                    print(f"\n--- Match #{i} ({item['timestamp']}) ---")
                    print(f"Query: {item['query']}")
                    print(f"\n{item['matches'][:300]}...")  # Show first 300 chars
            else:
                print("\n⚠ No match history found")
        
        elif choice == "4":
            # Update preferences
            profile = memory.get_user_profile(username)
            
            if profile:
                profile = update_profile(profile)
                memory.save_user_profile(username, profile)
                print("\n✓ Profile updated!")
            else:
                print("\n⚠ No profile found. Create one first (Option 1)")
        
        elif choice == "5":
            # List all users
            users = memory.list_all_users()
            
            if users:
                print("\n" + "=" * 60)
                print("Saved Users in Redis")
                print("=" * 60)
                for user in users:
                    profile = memory.get_user_profile(user)
                    print(f"  • {user}: {profile.get('name', 'N/A')}")
            else:
                print("\n⚠ No users saved yet")
        
        elif choice == "6":
            # Delete profile
            confirm = input(f"\nAre you sure you want to delete {username}'s profile? (yes/no): ").strip().lower()
            if confirm == "yes":
                memory.delete_user_profile(username)
                print("✓ Profile deleted")
            else:
                print("✗ Cancelled")
        
        elif choice == "7":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n⚠ Invalid option. Please try again.")


if __name__ == "__main__":
    main()
