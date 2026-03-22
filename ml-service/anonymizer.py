import spacy
import re

# We are loading a pre-trained language "brain" from spaCy. 
# It understands English words, names, organizations, and grammar out of the box.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spaCy model 'en_core_web_sm' not found. Make sure to download it using: python -m spacy download en_core_web_sm")
    nlp = None

# The Skill Dictionary (Moved from extractor to strictly protect skills during anonymization)
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


# 🌟 These are gendered words we want to remove.
# If the AI reads "he led a team", it might subconsciously prefer men. We remove this.
GENDER_WORDS = [
    "he", "she", "him", "her", "his", "hers", "himself", "herself",
    "mr", "mr.", "mrs", "mrs.", "ms", "ms."
]

# 🌟 Skills we should NEVER redact (The Whitelist)
# We don't want to accidentally scrub "Java" thinking it's a Person!
SKILLS_WHITELIST = {
    "java", "python", "sql", "postgresql", "mysql", "javascript", "react", "node", "express",
    "docker", "kubernetes", "linux", "aws", "gcp", "azure", "git", "github", "html", "css",
    "numpy", "pandas", "ai", "machine learning", "spring", "boot", "jdbc", "next.js", "supabase",
    "achievements", "details", "board", "merit", "scholarship", "languages", "technologies",
    "ug", "pg", "hsc", "ssc", "graduat", "experience", "education", "project",
    "chemistry", "department", "examination", "system", "school", "college", "youtube",
    "firebase", "forecasting", "iiird", "10th", "12th", "mpbse", "cbse", "icse",
    "university", "institute", "training", "internship", "developer", "engineer"
}

def anonymize_text(text: str) -> dict:
    """
    Takes raw resume text and removes all Personally Identifiable Information (PII).
    This is so the AI evaluates SKILLS only, not the PERSON.
    """
    doc = nlp(text)
    
    redacted_items = {
        "names": [],
        "organizations": [],
        "locations": []
    }

    anonymized = text
    
    # 2. Iterate through entities found by the AI brain
    # We sort entities by length (longest first) to avoid partial replacement bugs
    for ent in sorted(doc.ents, key=lambda x: len(x.text), reverse=True):
        word_clean = ent.text.strip().lower()
        
        # 🚨 THE BRAIN FIX: If the word is a known tech skill OR the AI labeled it as a SKILL, skip it!
        if ent.label_ == "SKILL" or word_clean in SKILLS_WHITELIST or any(skill in word_clean for skill in SKILLS_WHITELIST):
            continue
            
        # Only redact if it looks like a real entity (length > 2 for names/orgs)
        if ent.label_ == "PERSON" and len(ent.text) > 3:
            if ent.text in anonymized:
                redacted_items["names"].append(ent.text)
                anonymized = anonymized.replace(ent.text, "[NAME]")
        
        elif ent.label_ == "ORG" and len(ent.text) > 2:
            if ent.text in anonymized:
                redacted_items["organizations"].append(ent.text)
                anonymized = anonymized.replace(ent.text, "[ORG]")
        
        elif ent.label_ in ("GPE", "LOC") and len(ent.text) > 2:
            if ent.text in anonymized:
                redacted_items["locations"].append(ent.text)
                anonymized = anonymized.replace(ent.text, "[LOCATION]")

    # 3. Remove gendered pronouns
    for word in GENDER_WORDS:
        anonymized = re.sub(r'\b' + re.escape(word) + r'\b', "[PRONOUN]", anonymized, flags=re.IGNORECASE)

    return {
        "anonymized_text": anonymized,
        "redacted_items": redacted_items
    }
