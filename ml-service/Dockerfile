# Use the official lightweight Python image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the image
COPY requirements.txt .

# Install system and python dependencies (CPU-only versions for smallest footprint)
RUN apt-get update && apt-get install -y libomp-dev && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY . .

# Run the training script on build to generate the XGBoost model
RUN python predictor.py

# Expose the API port
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
