# PKI-Based 2FA Microservice (Dockerized)

This project implements a secure PKI-based Two-Factor Authentication (2FA) microservice using **RSA-4096**, **TOTP**, **Docker**, **FastAPI**, and **cron**.  
It satisfies all requirements from the Partnr PKI–2FA assignment.

---

## 🔐 Features

- RSA-4096 key pair (student)
- Decrypt encrypted seed using **RSA/OAEP + SHA-256**
- Generate 6-digit TOTP codes (SHA-1, 30-second window)
- Verify codes with ±1 period tolerance
- Seed stored persistently at `/data/seed.txt`
- Cron job logs TOTP codes every minute to `/cron/last_code.txt`
- Fully containerized with a multi-stage Dockerfile

---

## 📡 API Endpoints

### **POST /decrypt-seed**
Decrypts the encrypted seed and stores it at `/data/seed.txt`.

### **GET /generate-2fa**
Generates the current TOTP code and the number of seconds remaining.

### **POST /verify-2fa**
Verifies a given TOTP code with ±30s tolerance.

---

## 🐳 Running with Docker

### **Build & start**
```bash
docker-compose build
docker-compose up -d
