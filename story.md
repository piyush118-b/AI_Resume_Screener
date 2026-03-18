# The Evolution of the Auditor

Building a resume screener sounds straightforward until you try to make it objective. This project started with a simple question: Can we build a hiring tool that ignores who a person is and focus entirely on what they can do? This is the history of how we built, broke, and eventually refined the AI Resume Screener.

## The Beginning
The original vision was to create a standard NLP-based resume scanner using Java for the backend and Python for the ML brain. We wanted semantic similarity—meaning if a job asks for "Frontend expertise," the system should understand that "React and Tailwind" is a 100% match even if the words don't overlap. We integrated sentence-transformers and XGBoost to handle the heavy lifting.

## The First Wall: The Identity Crisis
The first major technical hurdle was the Bias Engine. We built an anonymizer to strip names, genders, and locations before scoring. However, we quickly hit a wall where the anonymization was too aggressive. It started redacting technical skills like "Skill Lab" or specific project names, thinking they were organizations or proper nouns. This led to "False Positives" where the candidate's score dropped not because of bias, but because the AI was hiding their actual work.

## The Deployment Failure
When we moved from local development to the cloud (AWS EC2), we hit a second, much harder wall: Resource Exhaustion. Our 8GB instance immediately ran out of disk space. We discovered that standard PyTorch installations were downloading nearly 4GB of NVIDIA CUDA libraries that the server didn't even have hardware for. 

The build failed three times in a row with "No space left on device" errors. We had to pivot our entire deployment strategy. We stripped the Docker images, forced CPU-only installations, and implemented a sequential build process to ensure the server never peaked its disk usage. This was the moment the project moved from a local script to a hardened cloud application.

## Syncing the Brains
Once deployed, we noticed the "Neutral Match" scores were almost identical to the standard ones. The model was so robust that redacting a few name tokens didn't shift the vector meaning. To solve this, we had to "Sync the Brains." We refactored the two distinct ML modules—the Anonymizer and the Extractor—to share a single NLP pipeline with a technical entity ruler. 

This synchronization ensured that anything recognized as a "Skill" was strictly protected from redaction. Only after this change did we see our first real "Bias Gap." In one test case, a candidate's score dropped from 31% to 22% once their identity markers were removed, proving that the identity-blind audit was finally working.

## The Result
What started as a simple keyword matcher ended as a multi-stage microservice architecture. We overcame memory leaks, library bloat, and logic conflicts between our NLP modules. The Auditor is now a tool that doesn't just scan resumes—it provides a transparent, accountable audit of the hiring process itself.
