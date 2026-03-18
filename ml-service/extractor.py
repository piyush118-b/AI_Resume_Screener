import spacy
import re

# We are loading a pre-trained language "brain" from spaCy. 
# It understands English words, names, organizations, and grammar out of the box.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spaCy model 'en_core_web_sm' not found. Make sure to download it using: python -m spacy download en_core_web_sm")
    nlp = None

# 🌟 1. The Skill Dictionary
KNOWN_SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "php", "ruby", "go", "rust", "kotlin", "swift",
    "spring boot", "spring", "django", "flask", "fastapi", "express", "node", "laravel", "rails", "asp.net",
    "react", "angular", "vue", "html", "css", "tailwind", "bootstrap", "jquery", "next.js", "redux",
    "sql", "postgresql", "mysql", "mongodb", "redis", "oracle", "sqlite", "cassandra", "firebase",
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible", "git", "github", "gitlab",
    "machine learning", "deep learning", "artificial intelligence", "nlp", "data science", "tensorflow", "pytorch", 
    "scikit-learn", "pandas", "numpy", "tableau", "power bi", "r", "opencv",
    "jira", "confluence", "postman", "swagger", "graphql", "rest api", "microservices", "agile", "scrum", "linux"
]

# Add a pattern matcher to the spacy brain!
if nlp:
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [{"label": "SKILL", "pattern": skill} for skill in KNOWN_SKILLS]
    ruler.add_patterns(patterns)


def format_skill_name(skill: str) -> str:
    """Makes sure skills like AWS, SQL, and PHP stay capitalized correctly."""
    UPPERCASE_SKILLS = ["aws", "sql", "php", "gcp", "nlp", "api", "html", "css", "js", "r", "it", "ece", "cse"]
    if skill.lower() in UPPERCASE_SKILLS:
        return skill.upper()
    return skill.title() # Capitalizes first letter (e.g., python -> Python)

def extract_skills(text: str) -> list[str]:
    """Uses the new Entity Brain to find skills much faster and smarter."""
    if not nlp:
        return []
        
    doc = nlp(text)
    found_skills = set()
    
    # 🌟 We look for things the AI labeled as "SKILL"
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            found_skills.add(format_skill_name(ent.text))
            
    return list(found_skills)

def extract_education(text: str) -> list[str]:
    """Tries to figure out what specific college degrees and branches the applicant has."""
    text_lower = text.lower()
    found_edu = set()
    found_branches = set()
    
    # 1. Degree Mapping
    EDU_MAP = {
        "bachelor": "Bachelor's Degree",
        "graduat": "Graduation", 
        "master": "Master's Degree",
        "phd": "PhD",
        "b.tech": "B.Tech",
        "m.tech": "M.Tech",
        "b.s": "B.S.",
        "m.s": "M.S.",
        "b.sc": "B.Sc",
        "m.sc": "M.Sc",
        "mba": "MBA",
        "b.e": "B.E.",
        "m.e": "M.E.",
        "diploma": "Diploma"
    }

    # 2. Branch/Specialization Mapping
    BRANCH_MAP = {
        "computer science": "Computer Science",
        "computer engineering": "Computer Engineering",
        "information technology": "Information Technology",
        "mechanical": "Mechanical",
        "civil": "Civil",
        "electrical": "Electrical",
        "electronics": "Electronics",
        "ece": "ECE",
        "cse": "CSE",
        "it": "IT"
    }
    
    # Search for Degrees
    for key, display_name in EDU_MAP.items():
        if re.search(r'\b' + re.escape(key), text_lower):
            found_edu.add(display_name)

    # Search for Branches
    for key, display_name in BRANCH_MAP.items():
        if re.search(r'\b' + re.escape(key) + r'\b', text_lower):
            found_branches.add(display_name)
            
    # Combine results for a better UI experience
    if not found_edu and not found_branches:
        return []
    
    # If we found both, return them together like "B.Tech (Computer Science)"
    if found_edu and found_branches:
        edu_str = ", ".join(found_edu)
        branch_str = ", ".join(found_branches)
        return [f"{edu_str} in {branch_str}"]
    
    return list(found_edu) if found_edu else list(found_branches)

def analyze_resume(text: str) -> dict:
    """
    The orchestrator function. It takes raw text and spits out structured data.
    This is the core of what AI/Data Extraction is!
    """
    # 🌟 Call our helper functions above
    skills = extract_skills(text)
    education = extract_education(text)
    
    # Package it into a neat Dictionary (which turns into JSON over the internet)
    return {
        "skills": skills,
        "education": education,
        "skill_count": len(skills) # A cool bonus metric: How many skills do they have?
    }
