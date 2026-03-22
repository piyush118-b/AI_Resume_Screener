from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import uvicorn
import fitz  # PyMuPDF
from extractor import analyze_resume        # NLP skill/education extraction
from matcher import calculate_match_score  # Vector embedding cosine similarity
from anonymizer import anonymize_text       # 🌟 NEW: Bias removal engine
from predictor import predict_placement     # 🌟 NEW: XGBoost Hiring predictor
import re

app = FastAPI(title="AI Resume Screener ML Service")

# 🌟 What does a Scoring Request look like?
# We create a 'Blueprint' so the internet knows exactly what data we need.
# We expect JSON that looks like {"resume_text": "...", "job_text": "..."}
class ScoreRequest(BaseModel):
    resume_text: str
    job_text: str

@app.get("/")
def health_check():
    return {"status": "ok", "service": "ML Microservice is running"}

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    # Wait for the entire PDF file to be sent over the internet to us
    content = await file.read() 
    
    try:
        # Open the PDF like a digital book
        doc = fitz.open(stream=content, filetype="pdf")
        
        # Read every page and squish the text into one giant string
        text = ""
        for page in doc:
            text += page.get_text()
            
        # 🌟 2. Send the raw string into our custom Extractor function!
        # It's like putting raw coffee beans into a grinder.
        analysis_result = analyze_resume(text)
        
        # 🌟 3. Return a clean JSON response package!
        # This is what Spring Boot will see.
        return {
            "filename": file.filename, 
            "status": "success",
            "extracted_data": analysis_result, # The gold: our skills and education arrays!
            "raw_text_length": len(text), # Just a little metadata for fun
            "text": text # IMPORTANT: We need this to send back for scoring!
        }
    except Exception as e:
        return {"error": str(e), "message": "Failed to parse PDF"}

@app.post("/score-match")
def score_match(request: ScoreRequest):
    """
    The ultimate endpoint! Give it the raw text of a resume and the raw text
    of a job description, and it will calculate how well they match.
    """
    try:
        # Step 1: Run the NLP Brain on the resume to extract skills
        analysis_result = analyze_resume(request.resume_text)

        # Step 2: Calculate the STANDARD score (resume with name still visible)
        standard_score = calculate_match_score(
            resume_text=request.resume_text,
            job_description_text=request.job_text
        )

        # 🌟 Step 3: BIAS DETECTION — Anonymize the resume text first
        anonymized_result = anonymize_text(request.resume_text)
        anonymized_text = anonymized_result["anonymized_text"]

        # Step 4: Calculate the UNBIASED score (resume with PII stripped out)
        unbiased_score = calculate_match_score(
            resume_text=anonymized_text,
            job_description_text=request.job_text
        )

        # Step 5: Calculate the bias gap — how much did PII affect the result?
        # If this number is high, something biased was in the resume!
        bias_gap = round(abs(float(standard_score) - float(unbiased_score)), 2)

        # Step 6: Extract Features for XGBoost Model (Experience and Education Level)
        skill_count = len(analysis_result["skills"])
        education_level = 0
        edu_lowercase = [e.lower() for e in analysis_result["education"]]
        if any("phd" in e for e in edu_lowercase):
            education_level = 4
        elif any(M in e for e in edu_lowercase for M in ["master", "m.tech", "m.sc", "m.s", "m.e", "mba"]):
            education_level = 3
        elif any(B in e for e in edu_lowercase for B in ["bachelor", "b.tech", "b.s", "b.sc", "b.e", "degree"]):
            education_level = 2

        # Try to find a simple regex for "X years of experience", otherwise default to 3
        exp_match = re.search(r'(\d+)\+?\s*years?(?:\s+of)?\s+experience', request.resume_text.lower())
        years_experience = int(exp_match.group(1)) if exp_match else 3

        # Step 7: Call the XGBoost predict_placement model!
        ml_prob = predict_placement(
            similarity_score=float(standard_score),
            years_experience=years_experience,
            education_level=education_level,
            skill_count=skill_count
        )

        # 🌟 Step 8: BALANCE THE PROBABILITY (Logic Update)
        # We don't want 99% if similarity is 0%. 
        # Weighted average: 60% importance to job match, 40% to general profile strength.
        balanced_prob = (ml_prob * 0.4) + (float(standard_score) * 0.6)
        
        # 🌟 Step 9: SKILL GAP ANALYSIS
        # Extract skills from job description too!
        job_analysis = analyze_resume(request.job_text)
        job_skills = set(job_analysis["skills"])
        resume_skills = set(analysis_result["skills"])
        
        missing_skills = list(job_skills - resume_skills)

        # Step 10: Bundle it all up!
        return {
            "status": "success",
            "candidate_name": analysis_result.get("name", "Unknown"), # 🌟 NEW
            "similarity_score_percentage": float(standard_score),
            "unbiased_score_percentage": float(unbiased_score),
            "placement_probability": round(float(balanced_prob), 2),
            "bias_gap": float(bias_gap),
            "redacted_items": anonymized_result["redacted_items"],
            "matched_skills": analysis_result["skills"],
            "missing_skills": missing_skills,
            "education": analysis_result["education"],
            "experience": analysis_result.get("experience", [])       # 🌟 NEW
        }
    except Exception as e:
        return {"error": str(e), "message": "Failed to calculate score"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
