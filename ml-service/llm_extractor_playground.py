import json
import logging
from typing import List, Optional
from pydantic import BaseModel, Field
import requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# ------------------------------------------------------------------
# 1. Define the Structured Data Models (Pydantic)
# This is what we want the LLM to strictly output.
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

# ------------------------------------------------------------------
# 2. Extract Data using local Llama 3.1
# ------------------------------------------------------------------
def extract_resume_data(resume_text: str) -> Optional[CandidateProfile]:
    logging.info("Sending resume to Llama 3.1 for structured extraction...")
    
    # We pass the JSON schema of our Pydantic model into the prompt
    schema_json = json.dumps(CandidateProfile.model_json_schema())
    
    prompt = f"""
    You are an expert technical AI recruiter. You will be given raw text extracted from a parsed resume.
    Your task is to extract the candidate's name, skills, experience, and education and format it exactly according to the provided JSON schema. 
    
    Follow these rules:
    1. Output ONLY valid JSON.
    2. Do NOT output any markdown blocks (like ```json), just the raw JSON string.
    3. Ensure the structure perfectly matches the schema.
    4. If a field is missing from the resume, return an empty string or empty list for that field.

    JSON Schema:
    {schema_json}
    
    Raw Resume Text:
    {resume_text}
    """

    # Hit the local Ollama API
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "format": "json", # Forces Ollama to output valid JSON
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        # Parse the JSON response from Llama
        result_text = response.json().get("response", "{}")
        
        # Llama might still sometimes wrap in markdown if "format":"json" isn't respected fully, 
        # so we strip it just in case
        if result_text.startswith("```json"):
            result_text = result_text.strip("```json").strip("```")

        # Load into Pydantic model to validate
        structured_data = json.loads(result_text)
        profile = CandidateProfile(**structured_data)
        return profile

    except Exception as e:
        logging.error(f"Failed to extract or parse data: {str(e)}")
        return None

# ------------------------------------------------------------------
# 3. Playground Execution
# ------------------------------------------------------------------
if __name__ == "__main__":
    # A chaotic, messy raw text example (similar to what PyMuPDF extracts from a bad PDF layout)
    chaotic_resume = """
    JOHN J. DOE - Full Stack Dev
    Contact: john.doe@email.com
    | TECH SKILLS: Java, Spring Boot, React, AWS, Docker | Kubernetes |
    
    Exp:
    Senior Software Eng.
    Amazon Web Services (AWS) - 01/2021 to Present
    * Built scalable microservices handling 10M+ requests/day.
    * Reduced DB latency by 40% using Redis.
    
    SDE 1 -> Tech Mahindra
    2018 - 2020. 
    Maintained legacy Java monolith. Wrote Junit tests.
    
    Edu: 
    B.S. in Computer Engg
    University of California, Berkeley (2018)
    """

    logging.info("Starting extraction test...")
    profile = extract_resume_data(chaotic_resume)
    
    if profile:
        logging.info("\n=== 🎉 SUCCESSFUL EXTRACTION 🎉 ===")
        # Print the beautified JSON validated by Pydantic
        print(profile.model_dump_json(indent=4))
    else:
        logging.error("Extraction returned None")
