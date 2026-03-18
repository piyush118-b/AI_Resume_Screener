# ☁️ AWS Deployment Guide: AI Resume Screener

This guide provides a step-by-step process to deploy the entire stack to AWS using **EC2** and **Docker Compose**.

## 🏗️ Architecture Overview
We will deploy a single EC2 instance running:
1.  **PostgreSQL 15** (Container)
2.  **FastAPI ML Brain** (Container)
3.  **Spring Boot Backend** (Container)

---

## 🚀 Step 1: Provision your EC2 Instance
1.  **Log in** to your [AWS Management Console](https://console.aws.amazon.com/).
2.  **Navigate to EC2** > **Launch Instance**.
3.  **Settings**:
    *   **Name**: `AI-Resume-Screener-Server`
    *   **AMI**: Ubuntu 24.04 LTS.
    *   **Instance Type**: `t3.small` (Recommended) or `t3.medium`.
        *   *Note: `t2.micro` may struggle with NLP model loading.*
    *   **Key Pair**: Create one and download the `.pem` file to your computer.
4.  **Network Settings (Security Group)**:
    *   Allow **SSH** (Port 22) from your IP.
    *   Allow **HTTP** (Port 80) from anywhere.
    *   Allow **Custom TCP** (Port 8080) from anywhere (for the dashboard).

---

## 🛠️ Step 2: Server Setup (SSH)
Connect to your server via Terminal:
```bash
chmod 400 your-key.pem
ssh -i "your-key.pem" ubuntu@your-ec2-ip
```

Install Docker & Docker Compose:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker ubuntu
newgrp docker
```

---

## 📦 Step 3: Deployment
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/piyush118-b/AI_Resume_Screener.git
    cd AI_Resume_Screener
    ```

2.  **Start the Services**:
    ```bash
    docker-compose up --build -d
    ```

3.  **Verify**:
    ```bash
    docker-compose ps
    ```

---

## 🌐 Step 4: Access your Application
Open your browser and navigate to:
`http://<YOUR_EC2_PUBLIC_IP>:8080/dashboard`

---

## 🛡️ Production Hardening (Optional)
### 1. Reverse Proxy (Nginx)
To use Port 80 instead of 8080, install Nginx on the host:
```bash
sudo apt install nginx -y
```
Create a config at `/etc/nginx/sites-available/resume-screener`:
```nginx
server {
    listen 80;
    server_name your-domain-or-ip;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. AWS RDS
For a more robust setup, migrate the database from a container to **AWS RDS (PostgreSQL)** for automated backups and scaling.
