"""Load people data from Excel (lessie_export.xlsx)"""

import pandas as pd
import json
from typing import List, Dict, Any


class ExcelDataLoader:
    """Load and manage people profiles from Excel file"""
    
    def __init__(self, file_path: str = "../lessie_export.xlsx"):
        """Initialize with path to Excel file"""
        self.file_path = file_path
        self.people = self._load_data()
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load people data from Excel file and convert to JSON-like format"""
        # Read Excel
        df = pd.read_excel(self.file_path, sheet_name='person_list')
        
        people = []
        for idx, row in df.iterrows():
            # Extract review data if available
            review_data = {}
            try:
                if pd.notna(row['Review']) and isinstance(row['Review'], str):
                    # Parse the review JSON
                    review_list = json.loads(row['Review'].replace("'", '"'))
                    review_data = {item['keypoint']: item['reason'] for item in review_list}
            except:
                pass
            
            # Extract skills/interests from multiple fields
            skills = []
            interests = []
            
            # Parse departments
            if pd.notna(row['Departments']):
                dept = str(row['Departments']).split(',')
                interests.extend([d.strip() for d in dept if d.strip()])
            
            # Parse title for skills
            if pd.notna(row['Title']):
                title = str(row['Title']).lower()
                # Extract common skills/roles from title
                skill_keywords = {
                    'product manager': ['Product Management', 'Strategy'],
                    'engineer': ['Engineering', 'Development'],
                    'designer': ['Design', 'UI/UX'],
                    'marketing': ['Marketing', 'GTM'],
                    'sales': ['Sales', 'BD'],
                    'ai': ['AI', 'Machine Learning'],
                    'ml': ['Machine Learning', 'AI'],
                    'data': ['Data Science', 'Analytics'],
                    'devops': ['DevOps', 'Infrastructure'],
                    'backend': ['Backend', 'Server'],
                    'frontend': ['Frontend', 'UI'],
                    'full stack': ['Full Stack', 'Development'],
                }
                for keyword, skill_list in skill_keywords.items():
                    if keyword in title:
                        skills.extend(skill_list)
            
            # Extract headline insights
            if pd.notna(row['Headline']):
                headline = str(row['Headline']).lower()
                if 'ai' in headline or 'machine learning' in headline or 'genai' in headline:
                    if 'AI' not in skills:
                        skills.append('AI')
                if 'fraud' in headline:
                    interests.append('Fraud Detection')
                if 'fintech' in headline:
                    interests.append('FinTech')
                if 'saas' in headline:
                    interests.append('SaaS')
            
            # Determine experience level from title
            experience_level = 'intermediate'
            title_lower = str(row['Title']).lower() if pd.notna(row['Title']) else ''
            if 'senior' in title_lower or 'principal' in title_lower or 'director' in title_lower:
                experience_level = 'advanced'
            elif 'associate' in title_lower or 'junior' in title_lower:
                experience_level = 'beginner'
            
            # Deduplicate
            skills = list(dict.fromkeys(skills)) if skills else ['General']
            interests = list(dict.fromkeys(interests)) if interests else ['Technology']
            
            # Create person object
            person = {
                "id": idx + 1,
                "name": row.get('Name', f'Person {idx+1}'),
                "title": str(row.get('Title', 'Unknown')) if pd.notna(row.get('Title')) else 'Unknown',
                "company": str(row.get('Company', 'Unknown')) if pd.notna(row.get('Company')) else 'Unknown',
                "skills": skills,
                "interests": interests,
                "experience_level": experience_level,
                "role_preferences": [str(row.get('Title', 'General')).split('|')[0].strip()[:30]],
                "location": {
                    "city": str(row.get('City', '')) if pd.notna(row.get('City')) else '',
                    "state": str(row.get('State', '')) if pd.notna(row.get('State')) else '',
                    "country": str(row.get('Country/Region', '')) if pd.notna(row.get('Country/Region')) else ''
                },
                "email": str(row.get('Individual email', '')) if pd.notna(row.get('Individual email')) else '',
                "linkedin": str(row.get('Profile Link', '')) if pd.notna(row.get('Profile Link')) else '',
                "headline": str(row.get('Headline', '')) if pd.notna(row.get('Headline')) else '',
                "review_result": str(row.get('Review Result', '')) if pd.notna(row.get('Review Result')) else '',
                "review_data": review_data
            }
            
            people.append(person)
        
        print(f"✓ Loaded {len(people)} people from {self.file_path}")
        return people
    
    def get_all_people(self) -> List[Dict[str, Any]]:
        """Get all people"""
        return self.people
    
    def get_person_by_id(self, person_id: int) -> Dict[str, Any]:
        """Get person by ID"""
        for person in self.people:
            if person['id'] == person_id:
                return person
        return None
    
    def get_person_by_name(self, name: str) -> Dict[str, Any]:
        """Get person by name"""
        for person in self.people:
            if person['name'].lower() == name.lower():
                return person
        return None
    
    def get_people_with_skill(self, skill: str) -> List[Dict[str, Any]]:
        """Get people with a specific skill"""
        return [p for p in self.people if skill.lower() in [s.lower() for s in p.get('skills', [])]]
    
    def get_people_by_company(self, company: str) -> List[Dict[str, Any]]:
        """Get people from a specific company"""
        return [p for p in self.people if company.lower() in p.get('company', '').lower()]
    
    def get_people_by_location(self, city: str = None, state: str = None) -> List[Dict[str, Any]]:
        """Get people by location"""
        results = []
        for p in self.people:
            loc = p.get('location', {})
            if city and city.lower() in loc.get('city', '').lower():
                results.append(p)
            elif state and state.lower() in loc.get('state', '').lower():
                results.append(p)
        return results
    
    def format_person(self, person: Dict[str, Any]) -> str:
        """Format person data as readable string"""
        return f"""
Name: {person['name']}
Title: {person['title']}
Company: {person['company']}
Location: {person['location']['city']}, {person['location']['state']}
Skills: {', '.join(person.get('skills', []))}
Interests: {', '.join(person.get('interests', []))}
Experience: {person.get('experience_level', 'unknown')}
Review Result: {person.get('review_result', 'N/A')}
"""
