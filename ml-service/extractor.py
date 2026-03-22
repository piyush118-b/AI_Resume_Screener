import json
import logging
from typing import List, Optional
from pydantic import BaseModel, Field
import requests

# ------------------------------------------------------------------
# Define the Structured Data Models (Pydantic)
# ------------------------------------------------------------------
class Experience(BaseModel):
    role: str = Field(description="The job title or role")
    company: str = Field(description="The name of the company")
    years: str = Field(description="Detailed duration, e.g., '2020 - 2023' or '3 years'")
    achievements: List[str] = Field(description="List of key responsibilities or achievements")

class Education(BaseModel):
    degree: str = Field(description="The degree obtained, e.g., 'B.Tech in Computer Science'")
    institution: str = Field(description="The university or college name")
    year_of_passing: str = Field(description="The graduation year")

class CandidateProfile(BaseModel):
    name: str = Field(description="Full name of the candidate")
    skills: List[str] = Field(description="List of technical skills and tools")
    experience: List[Experience] = Field(description="List of work experiences")
    education: List[Education] = Field(description="List of educational qualifications")

def extract_resume_data(text: str) -> CandidateProfile:
    """Hits the local Llama 3.1 model to extract strict JSON from chaotic text."""
    schema_json = json.dumps(CandidateProfile.model_json_schema())
    
    prompt = f"""
    You are an expert technical AI recruiter. You will be given raw text extracted from a parsed resume or job description.
    Your task is to extract the candidate's name, skills, experience, and education and format it exactly according to the provided JSON schema. 
    
    Follow these rules:
    1. Output ONLY valid JSON.
    2. Do NOT output any markdown blocks (like ```json), just the raw JSON string.
    3. Ensure the structure perfectly matches the schema.
    4. If a field is missing from the resume, return an empty string or empty list for that field.

    JSON Schema:
    {schema_json}
    
    Raw Document Text:
    {text}
    """

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "format": "json",
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=60) # High timeout for LLM inference
        response.raise_for_status()
        
        result_text = response.json().get("response", "{}")
        if result_text.startswith("```json"):
            result_text = result_text.strip("```json").strip("```")

        structured_data = json.loads(result_text)
        return CandidateProfile(**structured_data)

    except Exception as e:
        logging.error(f"Failed to use LLM for extraction, falling back to empty. Error: {str(e)}")
        # Fallback profile
        return CandidateProfile(name="Unknown", skills=[], experience=[], education=[])

def analyze_resume(text: str) -> dict:
    """
    The orchestrator function. Takes raw text, runs it through the LLM,
    and spits out structured data matching the backend's expected API.
    """
    # 🌟 Call our new LLM brain
    logging.info("Calling Llama 3.1 Extractor...")
    profile = extract_resume_data(text)
    
    # Format the education list into simple strings for backend backward compatibility
    education_strings = [
        f"{edu.degree} at {edu.institution} ({edu.year_of_passing})" 
        for edu in profile.education
    ]
    
    # Convert experiences to pure dicts for JSON serialization
    experience_dicts = [exp.model_dump() for exp in profile.experience]

    # Package it into a neat Dictionary (which turns into JSON over the internet)
    return {
        "name": profile.name,
        "skills": profile.skills,
        "education": education_strings,
        "experience": experience_dicts, # 🌟 NEW HUGE ADDITION
        "skill_count": len(profile.skills)
    }
