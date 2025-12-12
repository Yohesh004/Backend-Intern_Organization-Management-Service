# Organization Management Service – Backend (FastAPI + MongoDB)

This project implements a multi-tenant Organization Management backend designed to support platforms where each organization requires isolated data storage, secure admin authentication, and scalable database management. It is built using **FastAPI**, **MongoDB**, **JWT authentication**, and **bcrypt password hashing**.

The design prioritizes modularity, clarity, and horizontal scalability, making it suitable for SaaS-style applications.

---

## 🚀 Features
- Create organizations with isolated databases (`org_<name>`)
- Secure admin creation with bcrypt-hashed passwords
- JWT-based authentication
- Dynamic database creation, migration, and deletion
- Centralized master database for metadata
- Clean modular project structure (routes, repository, models, config)
- Fully async using Motor (MongoDB async driver)

---

## 🛠️ Tech Stack
- **FastAPI** (Python)
- **MongoDB**
- **Motor**
- **JWT**
- **bcrypt**
- **Pydantic**

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

Else:
```
"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe"
```

---

### 5️⃣ Run the Server
```
uvicorn app.main:app --reload --port 8000
```

Open API docs at:
👉 http://127.0.0.1:8000/docs

---

## 📘 API Documentation Summary

### **POST /org/create**
Create organization + admin.

### **GET /org/get**
Fetch organization metadata.

### **PUT /org/update** *(JWT required)*
Rename organization + migrate data.

### **DELETE /org/delete** *(JWT required)*
Delete organization + dynamic database.

### **POST /admin/login**
Admin login → returns JWT.

---

# 🧠 High-Level Architecture Overview

This backend uses a **multi-tenant architecture** where each organization has its own MongoDB database.  
The master database holds global metadata and authentication information.

### Key Components:
- **FastAPI Backend**
- **Master Database**
- **Dynamic Organization Databases**
- **JWT Auth Layer**
- **Repository Layer**

---

# 🏗️ High-Level Architecture Diagram
> Place your image inside `/assets/`

```
assets/High_level_Architecture.png
```

---

# 📊 Supporting Output Screenshots

### MongoDB Compass – Master DB
```
assets/Mangodb_compass_output.png
```

### MongoDB Compass – Dynamic Org DB
```
assets/Mangodb_compass_output2.png
```

### Terminal Output
```
assets/terminal_output.png
```

### POST /org/create Example
```
assets/POST_config.png
```

### Admin Auth Example
```
assets/admin_auth_config.png
```

---

# 📈 Scalability & Design Choices

This architecture is scalable because:

- Each tenant has an isolated database  
- Easy horizontal scaling  
- Secure boundaries between organizations  
- Clean modular backend  

### Trade-Offs:
- More databases = more ops overhead  
- Migration may be expensive on large datasets  
- Sharding may be needed at very high scale  

---

# 🎉 Conclusion

This backend fully meets the assignment requirements:

✔ Clean, modular, class-based structure  
✔ Dynamic multi-tenant DB creation  
✔ Secure bcrypt + JWT authentication  
✔ Complete documentation and architecture diagram  
✔ Screenshots provided for verification  

---
