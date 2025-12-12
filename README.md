# Organization Management Service – Backend (FastAPI + MongoDB)

This project implements a multi-tenant Organization Management backend designed for platforms where each organization requires isolated data storage, secure authentication, and scalable database management.  
It is built using **FastAPI**, **MongoDB**, **JWT**, and **bcrypt**.

The backend is modular, cleanly structured, and suitable for SaaS-style applications.

---

## 🚀 Features
- Organization creation with isolated MongoDB databases  
- Secure admin creation (bcrypt hashed passwords)  
- JWT-based authentication  
- Dynamic DB creation, migration, and deletion  
- Centralized master database  
- Asynchronous operations with Motor  
- Modular routing + repository pattern  

---

## 🛠️ Tech Stack
- FastAPI  
- MongoDB  
- Motor  
- bcrypt  
- JWT  
- Pydantic  

---

## 📂 Project Structure
```
app/
│── main.py
│── config.py
│── database.py
│── auth.py
│
├── models/
│   └── schemas.py
│
├── repositories/
│   └── org_repository.py
│
└── routes/
    ├── admin_routes.py
    └── org_routes.py

requirements.txt
.env.example
README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment
```
python -m venv venv
```

Activate:

**Windows**
```
venv\Scripts\activate
```

**Mac/Linux**
```
source venv/bin/activate
```

---

### 2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

---

### 3️⃣ Configure Environment Variables

Copy `.env.example` → `.env`

```
MONGO_URI=mongodb://localhost:27017
MASTER_DB=master_db
JWT_SECRET=your_secret_key
```

---

### 4️⃣ Start MongoDB

If installed as a service:
```
net start MongoDB
```

Or run manually:
```
"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe"
```

---

### 5️⃣ Run the Server
```
uvicorn app.main:app --reload --port 8000
```

Open API docs:

👉 http://127.0.0.1:8000/docs

---

# 🧠 High-Level Architecture Overview

This backend uses a **multi-tenant architecture**:

- Each organization gets its own MongoDB database  
- The master database stores global configuration + admin metadata  
- The repository layer handles DB operations  
- JWT ensures secure admin-level actions  
- Design ensures scalability and modularity  

---

# 🏗️ High-Level Architecture Diagram

<p align="center">
  <img src="/assets/High_level_Architecture.png" width="800">
</p>

---

# 📊 Supporting Output Screenshots

## 🗄️ MongoDB Compass – Master DB
<p align="center">
  <img src="Mangodb_compass_output.png" width="800">
</p>

---

## 🗄️ MongoDB Compass – Dynamic Org DB
<p align="center">
  <img src="Mangodb_compass_output2.png" width="800">
</p>

---

## 💻 Terminal Output – Running the Backend
<p align="center">
  <img src="terminal_output.png" width="800">
</p>

---

## 📬 POST /org/create Example
<p align="center">
  <img src="POST_config.png" width="800">
</p>

---

## 🔐 Admin Authentication Example
<p align="center">
  <img src="admin_auth_config.png" width="800">
</p>

---

# 📈 Scalability & Design Choices

### ✔ Strengths
- Strong data isolation  
- Easy to delete or migrate orgs  
- Scales horizontally across DB clusters  
- Clean modular backend  
- Secure authentication  

### ✔ Trade-offs
- More databases = more operational overhead  
- Migrations can be expensive  
- Very large systems may require sharding  

### ✔ For extreme scale (>10k orgs)
A hybrid shared-tenant + sharded architecture is recommended.

---

# 🎉 Conclusion

This backend fulfills all assignment requirements:

✔ Clean modular architecture  
✔ FastAPI + MongoDB implementation  
✔ JWT & bcrypt authentication  
✔ Dynamic multi-tenant DB management  
✔ Architecture diagram + screenshots included  

---
