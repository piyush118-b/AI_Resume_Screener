# 🤖 AI Resume Screener: The Auditor

[![AWS Deployment](https://img.shields.io/badge/Deployment-AWS_EC2-orange?logo=amazon-aws)](https://aws.amazon.com/)
[![Dockerized](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligence layer for modern hiring. This project isn't just a keyword matcher; it's a full-stack **Decision Support System** that uses NLP and Machine Learning to audit candidates with a focus on **Fairness** and **Predictive Accuracy**.

---

## 🌿 Core Features

### 1. ⚖️ Bias Detection & Fairness Engine
Most recruiters subconsciously prefer certain names or universities. **The Auditor** proactively fights this:
*   **PII Scrubbing**: Automatically redacts names, organizations, locations, and gendered pronouns using spaCy's NER (Named Entity Recognition).
*   **Neutral Screening**: Calculates a second score based *only* on the anonymized text.
*   **Bias Gap Analysis**: Flags if a candidate's identity influenced their score by more than 5%.

### 🎯 2. Hiring Prediction (XGBoost)
Uses a model trained on **4,500 real-world resumes** (trained in Google Colab) to predict the probability of a candidate successfully passing an HR screening.
*   **Inputs**: Skill count, education level, years of experience, and job similarity.
*   **Algorithm**: Gradient Boosting (XGBoost) for high-precision classification.

### 🔍 3. Skill Gap Analysis
Goes beyond what you have. It identifies what you **lack**:
*   Compares resume embeddings against the Job Description.
*   Lists "Missing Skills" in a dedicated dashboard section to help candidates or HR identify developmental areas.

---

## 🏗️ System Architecture

*   **Frontend**: Handcrafted, "Impeccable Style" dashboard using **Thymeleaf**, **Tailwind CSS**, and **Chart.js**.
*   **Backend (The Orchestrator)**: Robust **Java Spring Boot 3.x** microservice managing PDF processing and database persistence.
*   **ML Brain (The Auditor)**: Python **FastAPI** service handling:
    *   `sentence-transformers` (all-MiniLM-L6-v2) for vector embeddings.
    *   `spaCy` for high-speed NLP and NER.
    *   `XGBoost` for predictive modeling.
*   **Database**: **PostgreSQL 15** for reliable storage of every audit result.

---

## 🚀 Quick Start (Docker Compose)

The easiest way to run the entire stack locally is using Docker.

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/piyush118-b/AI_Resume_Screener.git
    cd AI_Resume_Screener
    ```

2.  **Launch the System**:
    ```bash
    docker-compose up --build
    ```

3.  **Access the Dashboard**:
    Open [http://localhost:8080/dashboard](http://localhost:8080/dashboard) in your browser.

---

## ☁️ Deployment (AWS)
This project is architected for the cloud. See the **[aws_deployment_guide.md](./aws_deployment_guide.md)** for detailed instructions on launching an EC2 instance with multi-container orchestration.

---

## 📈 Future Roadmap
- [ ] Integration with LinkedIn API for one-click auditing.
- [ ] Support for multi-language resumes (using BERT multilingual models).
- [ ] Comparison View: Audit 5 candidates side-by-side.

*Designed with ❤️ for fair and efficient hiring.*
