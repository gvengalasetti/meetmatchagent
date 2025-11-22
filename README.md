# 🤝 MeetMatch AI - Hackathon Team Matching Agent

An intelligent agentic search system that matches hackathon participants into optimal teams using Claude AI and Redis memory for persistent storage.

## 🚀 Live Demo

**Try it now:** [https://meetmatch-ai-527682779120.us-west1.run.app/](https://meetmatch-ai-527682779120.us-west1.run.app/)

> The live application provides an interactive web interface to create your profile and discover ideal teammates for hackathons using AI-powered matching.

## 💡 Key Idea

MeetMatch AI solves the common problem of finding compatible teammates for hackathons by leveraging:
- **Agentic AI**: Claude AI autonomously searches and reasons about optimal team compositions
- **Intelligent Matching**: Analyzes skills, interests, experience levels, and role preferences
- **Persistent Memory**: Redis-backed storage maintains user profiles and match history
- **Real Data**: 69+ hackathon participants from LinkedIn profiles via Sanity CMS

Instead of manual team formation, MeetMatch AI acts as an intelligent matchmaker that understands what makes great teams work together.

## ✨ Features

✨ **Agentic Search** - Claude AI agent intelligently searches and matches people based on skills, interests, and experience levels
🧠 **Redis Memory** - Persistent storage of user profiles and match history
🔄 **Profile Management** - Create, update, and manage multiple personas
📊 **Team Analysis** - Evaluates team compatibility and suggests balanced team structures
🔗 **LinkedIn Integration** - Data sourced from Sanity with LinkedIn enrichment
🌐 **Web Interface** - User-friendly web UI for profile creation and match discovery

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

## 🤖 How the Agentic System Works

The agent performs an intelligent multi-step agentic search using LangChain and Claude AI:

### Step-by-Step Process

1. **Profile Creation** 
   - You define your skills, interests, experience level, and team preferences
   - Profile is saved to Redis for future sessions

2. **Agentic Search Initialization**
   - Claude AI receives your profile and matching requirements
   - The agent autonomously plans its search strategy

3. **Tool-Based Search** 
   
   The AI agent has access to 5 specialized tools:
   
   | Tool | Purpose | Example |
   |------|---------|---------|
   | `search_people_by_skill` | Find people with specific technical skills | "Python", "Machine Learning" |
   | `search_people_by_interest` | Find people with shared interests | "Healthcare", "AI" |
   | `search_people_by_role` | Find people seeking specific roles | "Backend Developer" |
   | `get_all_people` | Access full participant database | Returns all 69 participants |
   | `calculate_team_fit` | Evaluate team compatibility | Analyzes skill overlap & diversity |

4. **Autonomous Reasoning**
   - The agent iteratively uses tools to gather information
   - Claude synthesizes search results using reasoning about:
     - Complementary skills (what you need vs what they have)
     - Shared interests (common ground for collaboration)
     - Experience balance (mixing levels for mentorship)
     - Role coverage (ensuring all needed roles are filled)

5. **Match Recommendations**
   - Returns 3 best matches with detailed explanations
   - Each match includes why they're a good fit
   - Considers both technical compatibility and personal alignment

6. **Persistent Memory**
   - Results saved to Redis with timestamps
   - Match history available for review
   - Profile reusable across sessions

### Example Agent Execution Flow

```
User Profile: "Python, ML, Healthcare" → intermediate → looking for "backend & frontend"
                                    ↓
Agent Plan: "Search complementary skills and healthcare interest"
                                    ↓
Tool Call 1: search_people_by_skill("Backend")
            → Returns: [Alex, Bob, Carol, ...]
                                    ↓
Tool Call 2: search_people_by_interest("Healthcare")
            → Returns: [David, Emily, Alex, ...]
                                    ↓
Tool Call 3: calculate_team_fit([Alex, Emily, Frank], "need frontend + backend")
            → Returns: Skill coverage analysis
                                    ↓
Agent Reasoning: "Alex has backend + healthcare interest, Emily frontend + healthcare, Frank DevOps"
                                    ↓
Final Output: Top 3 matches with explanations
```

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

## 🧪 Testing

### Test the CLI Application

1. **Run the interactive CLI**:
   ```bash
   python3 run_with_memory.py
   ```

2. **Create a test profile**:
   - Username: `testuser`
   - Skills: `Python, Machine Learning, Backend`
   - Interests: `AI, Healthcare, Startups`
   - Experience: `intermediate`
   - Role preferences: `ML Engineer, Backend Developer`
   - Looking for: `Frontend developers and designers for a health tech project`

3. **Verify AI matching**:
   - The agent should return 3 recommended matches
   - Each match should have a clear explanation of why they're a good fit
   - Results are automatically saved to Redis

4. **Test persistence**:
   - Exit and restart `run_with_memory.py`
   - Use the same username
   - Choose option 2 to view your saved profile
   - Choose option 3 to view match history

### Test Individual Components

**Test the AI Agent**:
```bash
python3 agent_new.py
```

**Test Data Loading**:
```bash
python3 -c "from excel_data_loader import ExcelDataLoader; loader = ExcelDataLoader('../lessie_export.xlsx'); print(f'Loaded {len(loader.get_all_people())} people')"
```

**Test Redis Connection**:
```bash
redis-cli ping  # Should return PONG
python3 -c "from redis_memory import RedisMemory; mem = RedisMemory()"
```

### Run Automated Tests

```bash
# Install test dependencies (if available)
pip install pytest pytest-cov

# Run tests (if test files exist)
pytest tests/ -v
```

## 🚢 Deployment

### Deploy to Google Cloud Run

1. **Prerequisites**:
   - Google Cloud account with billing enabled
   - `gcloud` CLI installed and configured
   - Docker installed (for container builds)

2. **Set up environment**:
   ```bash
   # Set your project ID
   export PROJECT_ID=your-project-id
   export REGION=us-west1
   
   # Configure gcloud
   gcloud config set project $PROJECT_ID
   ```

3. **Build container image**:
   ```bash
   # Create a Dockerfile (example provided below)
   docker build -t gcr.io/$PROJECT_ID/meetmatch-ai:latest .
   
   # Push to Google Container Registry
   docker push gcr.io/$PROJECT_ID/meetmatch-ai:latest
   ```

4. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy meetmatch-ai \
     --image gcr.io/$PROJECT_ID/meetmatch-ai:latest \
     --platform managed \
     --region $REGION \
     --allow-unauthenticated \
     --set-env-vars "ANTHROPIC_API_KEY=your-key-here" \
     --memory 512Mi \
     --timeout 300
   ```

5. **Get your service URL**:
   ```bash
   gcloud run services describe meetmatch-ai \
     --platform managed \
     --region $REGION \
     --format 'value(status.url)'
   ```

### Example Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port (Cloud Run expects PORT env var)
ENV PORT=8080
EXPOSE 8080

# Run the application
CMD ["python3", "run_with_memory.py"]
```

### Deploy to Other Platforms

**AWS Lambda with API Gateway**:
1. Package application with dependencies
2. Create Lambda function with Python 3.10 runtime
3. Set environment variables (ANTHROPIC_API_KEY)
4. Configure API Gateway for HTTP endpoints
5. Use AWS ElastiCache for Redis

**Heroku**:
```bash
# Login to Heroku
heroku login

# Create app
heroku create meetmatch-ai

# Add Redis addon
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=your-key-here

# Deploy
git push heroku main
```

**Railway**:
1. Connect GitHub repository to Railway
2. Add Redis plugin from Railway marketplace
3. Set ANTHROPIC_API_KEY environment variable
4. Deploy automatically on git push

## 🖼️ Screenshots

### Web Interface
*Note: The web application UI provides an intuitive interface for creating profiles and finding matches. Visit [the live demo](https://meetmatch-ai-527682779120.us-west1.run.app/) to see it in action.*

### CLI Interface
```
============================================================
🎯 HACKATHON TEAM MATCHING AGENT (with Redis Memory)
============================================================

1. Create/Update Profile & Find Matches
2. View Your Profile
3. View Match History
4. Update Profile Preferences
5. View All Saved Users
6. Delete Profile
7. Exit

Choose an option (1-7): 1

📝 Creating new profile for testuser
Your name: Sarah Chen
Your skills (comma-separated): Python, Machine Learning, Data Science
Your interests (comma-separated): AI, Healthcare, Climate Tech
Experience level (beginner/intermediate/advanced): intermediate
Role preferences (comma-separated): ML Engineer, Data Scientist
What are you looking for in a team? Looking for frontend and backend engineers to build a healthcare AI application

🔍 Finding matches for Sarah Chen...
------------------------------------------------------------

✅ Match Results:

Based on your profile, here are the 3 best team matches:

1. **Krishna Yalamanchili** (Principal ML Engineer, Advanced) - Deep ML expertise with AI/Engineering skills complements your data science background perfectly for healthcare AI development.

2. **Alex Rodriguez** (Senior Backend Engineer, Advanced) - Strong backend development and API design skills fill the technical gap you're looking for, with experience in healthcare systems.

3. **Emily Watson** (Frontend Developer, Intermediate) - React and UI/UX expertise provides the frontend capabilities your team needs, with interest in health tech projects.

💾 Results saved to Redis memory
```

## 🔧 Troubleshooting

**"Could not find matches"** - Check Redis connection and ensure participant data is loaded
**Redis connection refused** - Make sure Redis is running: `redis-cli ping` should return PONG
**API key errors** - Verify ANTHROPIC_API_KEY is set in .env file
**Excel file not found** - Ensure `lessie_export.xlsx` is in the correct directory
**Cloud Run deployment fails** - Check container logs: `gcloud run services logs read meetmatch-ai`

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Application                       │
│          (Cloud Run - meetmatch-ai)                     │
│         https://meetmatch-ai-...run.app/                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              run_with_memory.py                         │
│         (Interactive CLI Interface)                      │
│    • User profile creation & management                  │
│    • Match history tracking                              │
│    • 7 menu options for user interaction                 │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│ redis_memory.py │     │  agent_new.py   │
│  (Persistence)  │     │  (AI Matching)  │
├─────────────────┤     ├─────────────────┤
│ • User profiles │     │ • Claude Sonnet │
│ • Match history │     │ • 5 search tools│
│ • Redis storage │     │ • LangChain     │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                    ┌─────────────────────┐
                    │ excel_data_loader.py│
                    │   (Data Layer)      │
                    ├─────────────────────┤
                    │ • 69 participants   │
                    │ • LinkedIn data     │
                    │ • Sanity CMS export │
                    │ • Skills & interests│
                    └─────────────────────┘
```

### Component Details

1. **Web Application**: Cloud Run deployment with web interface for easy access
2. **CLI Interface**: Interactive command-line menu for profile and match management
3. **Redis Memory**: Persistent storage layer for user data and match history
4. **AI Agent**: Claude AI with specialized tools for intelligent team matching
5. **Data Layer**: Curated database of hackathon participants with enriched profiles

## Technologies

- **LangChain** - Agentic framework for building AI agents
- **Claude AI (Sonnet 4)** - Language model for intelligent matching and reasoning
- **Redis** - In-memory data store for fast profile and history access
- **Sanity** - Headless CMS for data management and enrichment
- **Pandas** - Excel data processing and manipulation
- **Python 3.10+** - Core programming language
- **Google Cloud Run** - Serverless container deployment platform

## 📊 Dataset Information

The application uses a curated dataset of 69 hackathon participants:
- **Source**: LinkedIn profiles via Sanity CMS
- **File**: `lessie_export.xlsx`
- **Fields**: Name, Title, Company, Skills, Interests, Experience Level, Location, LinkedIn URL
- **Update Frequency**: Manually curated and enriched
- **Privacy**: Public LinkedIn data only

To add more participants:
1. Export data from Sanity or LinkedIn
2. Format as Excel with required columns
3. Update `lessie_export.xlsx`
4. Restart the application

## 🙏 Acknowledgments

- Built with [Claude AI](https://www.anthropic.com/claude) by Anthropic
- Powered by [LangChain](https://www.langchain.com/) agentic framework
- Data managed through [Sanity](https://www.sanity.io/) CMS
- Inspired by the challenges of hackathon team formation

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs**: Open an issue with details about the problem
2. **Suggest features**: Share ideas for improvements
3. **Add participants**: Help expand the database with more profiles
4. **Improve matching**: Enhance the AI agent's matching algorithms
5. **Documentation**: Help improve this README or add code comments

### Development Setup

```bash
# Clone repository
git clone https://github.com/gvengalasetti/meetmatchagent.git
cd meetmatchagent

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black .

# Lint code
flake8 .
```

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/gvengalasetti/meetmatchagent/issues)
- **Live Demo**: [https://meetmatch-ai-527682779120.us-west1.run.app/](https://meetmatch-ai-527682779120.us-west1.run.app/)
- **Documentation**: This README

## ❓ FAQ

**Q: How accurate are the matches?**
A: The AI agent uses sophisticated reasoning about skills, interests, and experience levels. Match quality depends on profile completeness and the available participant pool.

**Q: Can I use this for non-hackathon team building?**
A: Yes! The system works for any team formation scenario - projects, startups, study groups, etc.

**Q: How do I add my own participant data?**
A: Export your data as Excel with columns: Name, Title, Company, Skills (comma-separated), Interests (comma-separated), Experience Level. Replace or append to `lessie_export.xlsx`.

**Q: Is my profile data secure?**
A: Profiles are stored locally in Redis. For production use, implement authentication and encrypt sensitive data.

**Q: Can I customize the matching criteria?**
A: Yes! Modify the prompt in `agent_new.py` or add new tools to the agent for custom matching logic.

**Q: What's the cost of running this?**
A: Local development is free (except Anthropic API costs ~$0.01-0.05 per match). Cloud Run costs ~$5-20/month depending on usage.

---

Made with ❤️ for hackathon teams everywhere
