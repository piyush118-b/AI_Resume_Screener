# AI Resume Screener: The Auditor

![Project Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

**Live Demo**: [http://16.171.145.227:8080/dashboard](http://16.171.145.227:8080/dashboard)


The Auditor is an intelligence layer designed for modern hiring. Instead of simple keyword matching, it provides a full-stack decision support system that uses Natural Language Processing and Machine Learning to audit candidates with a focus on fairness and predictive accuracy.

## Core Capabilities

### Bias Detection and Fairness Engine
Standard recruitment often suffers from subconscious bias based on names or locations. The Auditor addresses this directly:
*   **PII Anonymization**: The system automatically redacts names, organizations, locations, and gendered pronouns using spaCy's Named Entity Recognition (NER).
*   **Neutral Screening**: It calculates a secondary match score based strictly on anonymized text.
*   **Bias Gap Analysis**: The system flags results where a candidate's identity appears to influence their match score by more than a 5% margin.

### Hiring Prediction using XGBoost
The system includes a predictive model trained on thousands of data points to estimate the probability of a candidate successfully passing an initial HR screening.
*   **Features**: The model analyzes skill count, education level, years of experience, and job similarity.
*   **Methodology**: It utilizes Gradient Boosting (XGBoost) to provide high-precision classification.

### Skill Gap Identification
The Auditor identifies not just what a candidate possesses, but what they lack. By comparing resume embeddings against a specific Job Description, it generates a "Missing Skills" dossier to help HR identify specific developmental areas or missing requirements.

---

## System Architecture

*   **Logic Layer**: A Java Spring Boot 3.x microservice that orchestrates PDF processing, business logic, and database persistence.
*   **Intelligence Layer**: A Python FastAPI service handling vector embeddings (sentence-transformers), NLP/NER (spaCy), and predictive modeling (XGBoost).
*   **Interface**: A handcrafted dashboard built with Thymeleaf, Tailwind CSS, and Chart.js for data visualization.
*   **Data Persistence**: PostgreSQL 15 for reliable storage of audit results and candidate profiles.

---

## Local Development

To run the full stack locally using Docker:

1.  Clone the repository:
    ```bash
    git clone https://github.com/piyush118-b/AI_Resume_Screener.git
    cd AI_Resume_Screener
    ```

2.  Launch the services:
    ```bash
    docker-compose up --build
    ```

3.  Access the dashboard:
    Navigate to `http://localhost:8080/dashboard` in your browser.

---

## Server Deployment (AWS EC2)

The project is optimized for deployment on cloud environments like AWS. 

### Recommended Configuration
*   **Instance**: t3.small or t3.medium (minimum 2GB RAM required for ML models).
*   **OS**: Ubuntu 22.04 LTS or Amazon Linux 2023.
*   **Storage**: At least 12GB EBS volume.

### Deployment Steps
1.  Install Docker and Docker Compose on your instance.
2.  Clone the repository and enter the directory.
3.  Because cloud instances often lack GPUs, the project is configured to use CPU-only versions of Torch and Transformers to minimize memory footprint.
4.  Run the sequential build process to avoid disk space peak issues:
    ```bash
    docker build -t ai_resume_screener-backend ./backend
    docker build -t ai_resume_screener-ml-service ./ml-service
    docker-compose up -d
    ```

---

## Future Development
Plans include integration with professional networking APIs for one-click auditing, support for multi-language resumes using multilingual BERT models, and a comparison view for auditing multiple candidates side-by-side.

## License
Distributed under the MIT License.
