"""LangChain agent for hackathon team matching"""

import json
from pathlib import Path
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
import os
from dotenv import load_dotenv
from excel_data_loader import ExcelDataLoader

load_dotenv()


# Load people data from Excel
data_loader = ExcelDataLoader("../lessie_export.xlsx")
PEOPLE_DATA = data_loader.get_all_people()


@tool
def search_people_by_skill(skill: str) -> list:
    """Search for people with a specific skill"""
    results = []
    for person in PEOPLE_DATA:
        if skill.lower() in [s.lower() for s in person["skills"]]:
            results.append({
                "name": person["name"],
                "skills": person["skills"],
                "interests": person["interests"],
                "experience_level": person["experience_level"]
            })
    return results


@tool
def search_people_by_interest(interest: str) -> list:
    """Search for people interested in a specific topic"""
    results = []
    for person in PEOPLE_DATA:
        if interest.lower() in [i.lower() for i in person["interests"]]:
            results.append({
                "name": person["name"],
                "skills": person["skills"],
                "interests": person["interests"],
                "experience_level": person["experience_level"]
            })
    return results


@tool
def search_people_by_role(role: str) -> list:
    """Search for people interested in a specific role"""
    results = []
    for person in PEOPLE_DATA:
        if role.lower() in [r.lower() for r in person["role_preferences"]]:
            results.append({
                "name": person["name"],
                "role_preferences": person["role_preferences"],
                "experience_level": person["experience_level"],
                "skills": person["skills"]
            })
    return results


@tool
def get_all_people() -> list:
    """Get all people in the database"""
    return [{
        "id": p["id"],
        "name": p["name"],
        "skills": p["skills"],
        "interests": p["interests"],
        "experience_level": p["experience_level"],
        "role_preferences": p["role_preferences"]
    } for p in PEOPLE_DATA]


@tool
def calculate_team_fit(people_names: list, preferences: str) -> str:
    """Calculate how well a group of people fit together based on preferences"""
    selected_people = [p for p in PEOPLE_DATA if p["name"] in people_names]
    
    if not selected_people:
        return "No matching people found"
    
    all_skills = []
    all_interests = []
    for person in selected_people:
        all_skills.extend(person["skills"])
        all_interests.extend(person["interests"])
    
    return f"""
Team Composition Analysis:
- Members: {', '.join([p['name'] for p in selected_people])}
- Combined Skills: {', '.join(set(all_skills))}
- Shared Interests: {', '.join(set(all_interests))}
- Experience Levels: {', '.join(set([p['experience_level'] for p in selected_people]))}
- Roles Covered: {', '.join(set([r for p in selected_people for r in p['role_preferences']]))}
"""


class HackathonMatchingAgent:
    """LangChain agent for matching people for hackathon teams"""
    
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env")
        
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            temperature=0.7,
            api_key=api_key
        )
        
        self.tools = [
            search_people_by_skill,
            search_people_by_interest,
            search_people_by_role,
            get_all_people,
            calculate_team_fit
        ]
        
        self.llm_with_tools = self.llm.bind_tools(self.tools)
    
    def match_person(self, user_profile: dict) -> dict:
        """
        Main agent function: Given a user profile, find the best matches
        
        Args:
            user_profile: {
                "name": str,
                "skills": list,
                "interests": list,
                "experience_level": str,
                "role_preferences": list,
                "preferences": str (what they're looking for)
            }
        """
        
        prompt = f"""
You are a hackathon team matching expert. QUICKLY find 3 BEST matches for this person.

USER:
- Name: {user_profile.get('name', 'Unknown')}
- Skills: {', '.join(user_profile.get('skills', []))}
- Interests: {', '.join(user_profile.get('interests', []))}
- Experience: {user_profile.get('experience_level', 'unknown')}
- Roles: {', '.join(user_profile.get('role_preferences', []))}
- Goal: {user_profile.get('preferences', 'complementary team')}

SEARCH FOR 3 BEST MATCHES:
1. Search people with skills they need
2. Search people with shared interests
3. Get top candidates
4. RETURN 3 MATCHES WITH WHY (stop after this - NO MORE SEARCHING)

Format: NAME (role/skills) - ONE sentence why they fit
"""
        
        messages = [HumanMessage(content=prompt)]
        
        # Agentic loop with tool execution
        max_iterations = 3
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            response = self.llm_with_tools.invoke(messages)
            messages.append(response)
            
            # Check if response has tool calls
            if not response.tool_calls:
                # Got response without tool calls, return it
                if response.content and len(response.content) > 10:
                    return {
                        "matches": response.content,
                        "success": True
                    }
            
            # Process tool calls
            if response.tool_calls:
                tool_executed = False
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_input = tool_call["args"]
                    
                    # Find and execute the tool
                    tool_func = next((t for t in self.tools if t.name == tool_name), None)
                    if tool_func:
                        tool_executed = True
                        tool_result = tool_func.invoke(tool_input)
                        # Use proper ToolMessage format
                        tool_message = ToolMessage(
                            content=json.dumps(tool_result) if isinstance(tool_result, (dict, list)) else str(tool_result),
                            tool_call_id=tool_call.get("id", str(hash(tool_name)))
                        )
                        messages.append(tool_message)
                
                # If no tools were executed, break to avoid infinite loop
                if not tool_executed:
                    break
        
        # Return last response content if we have it
        for msg in reversed(messages):
            if hasattr(msg, 'content') and isinstance(msg.content, str) and len(msg.content) > 10:
                return {
                    "matches": msg.content,
                    "success": True
                }
        
        return {
            "matches": "Could not find matches after max iterations",
            "success": False
        }


if __name__ == "__main__":
    agent = HackathonMatchingAgent()
    
    user_profile = {
        "name": "Sarah",
        "skills": ["Python", "Machine Learning"],
        "interests": ["AI", "Healthcare", "Startups"],
        "experience_level": "intermediate",
        "role_preferences": ["ML Engineer", "Data Scientist"],
        "preferences": "Looking for backend developers and DevOps engineers to build a healthcare AI product"
    }
    
    print("🤖 Starting Hackathon Matching Agent...\n")
    print(f"Finding matches for: {user_profile['name']}")
    print(f"Preferences: {user_profile['preferences']}\n")
    print("-" * 60)
    
    result = agent.match_person(user_profile)
    
    print("\n✅ Agent Recommendations:\n")
    print(result["matches"])
