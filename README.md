# MEETMATCH - Hackathon Team Matching Agent

An intelligent agentic search system that matches hackathon participants into optimal teams using Claude AI and Redis memory for persistent storage.

Demo: https://meetmatch-ai-527682779120.us-west1.run.app/

## Features

✨ **Agentic Search** - Claude AI agent intelligently searches and matches people based on skills, interests, and experience levels
🧠 **Redis Memory** - Persistent storage of user profiles and match history
🔄 **Profile Management** - Create, update, and manage multiple personas
📊 **Team Analysis** - Evaluates team compatibility and suggests balanced team structures
🔗 **LinkedIn Integration** - Data sourced from Sanity with LinkedIn enrichment using Agentic deep search

## Quick Start

### Prerequisites
- Python 3.10+
- Redis running on localhost:6379
- ANTHROPIC_API_KEY environment variable set

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis (if not running)
redis-server --daemonize yes

# Copy environment file
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY
```

### Usage

```bash
# Run interactive menu with Redis memory
python3 run_with_memory.py
```

Then:
1. Enter your username
2. Choose "Create/Update Profile & Find Matches"
3. Enter your skills, interests, and preferences
4. Agent finds your best team matches!

## Files

- **agent_new.py** - LangChain agentic agent with Claude AI integration and 5 search tools
- **redis_memory.py** - Redis storage manager for profiles and match history
- **excel_data_loader.py** - Loads hackathon participant profiles from Excel (sourced from Sanity)
- **run_with_memory.py** - Interactive CLI with 7 menu options
- **requirements.txt** - Python dependencies
- **lessie_export.xlsx** - Database of 69 participants with skills and interests

## Menu Options

1. **Create/Update Profile & Find Matches** - Create a profile and get AI-powered match recommendations
2. **View Your Profile** - See your saved profile from Redis
3. **View Match History** - See all your past match results
4. **Update Profile Preferences** - Modify specific profile fields
5. **View All Saved Users** - List all profiles stored in Redis
6. **Delete Profile** - Remove a profile from Redis
7. **Exit**

## Example Session

```
Enter username: guna
Connected to Redis ✓

Choose: 1
Creating new profile...
Skills: Python, AI, Machine Learning
Interests: Startups, Healthcare
Experience: advanced

🔍 Finding matches...

✅ Match Results:
1. Krishna Yalamanchili (Principal ML Engineer) - Advanced experience with AI/Engineering skills
2. Liz Kao (Principal Product Manager) - AI/Product Strategy expertise
3. Manoj Tiwari (Senior Technical Recruiter) - Tech recruiting and career mentorship
```

## How It Works

The agent performs an intelligent agentic search:

1. **Profile Creation** - You define your skills, interests, experience level, and team preferences
2. **Agentic Search** - Claude AI agent autonomously searches the database using specialized tools:
   - `search_people_by_skill` - Find people with specific skills
   - `search_people_by_interest` - Find people with shared interests
   - `search_people_by_role` - Find people seeking specific roles
   - `get_all_people` - Access the full participant database
   - `calculate_team_fit` - Evaluate team compatibility
3. **Agent Reasoning** - Claude synthesizes search results and returns 3 best matches with detailed reasoning
4. **Persistent Memory** - Results saved to Redis with timestamps for future reference

## Data Source

The participant database (lessie_export.xlsx) was built using:
- **Sanity** - CMS for managing and enriching participant data
- **LinkedIn** - Professional profiles and skill extraction
- **Data Processing** - Excel export with 69 hackathon participants

## Data Structure

### User Profile (Redis)
```json
{
  "name": "string",
  "skills": ["list", "of", "skills"],
  "interests": ["list", "of", "interests"],
  "experience_level": "beginner|intermediate|advanced",
  "role_preferences": ["list", "of", "roles"],
  "preferences": "what they're looking for"
}
```

### Match History (Redis)
```json
{
  "timestamp": "2025-11-21T14:30:00",
  "query": "user search query",
  "matches": "match results from agent"
}
```

## Environment Setup

Create a `.env` file with:
```
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

## Troubleshooting

**"Could not find matches"** - Check Redis connection and ensure participant data is loaded
**Redis connection refused** - Make sure Redis is running: `redis-cli ping` should return PONG
**API key errors** - Verify ANTHROPIC_API_KEY is set in .env file

## Architecture

```
run_with_memory.py
    ↓
redis_memory.py (Profile persistence)
    ↓
agent_new.py (Claude AI agentic search)
    ↓
excel_data_loader.py (69 participant database from Sanity/LinkedIn)
```

## Technologies

- **LangChain** - Agentic framework
- **Claude AI** - Language model for intelligent matching
- **Redis** - In-memory data store
- **Sanity** - CMS for data management
- **Pandas** - Excel data processing
- **Python 3.10+**

## License

MIT
