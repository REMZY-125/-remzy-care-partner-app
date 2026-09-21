# Remzy Care Partner App

A mobile-first workforce application for **Remzy Home Health Care** Care Partners.

**WORK → CARE → VERIFY → LEARN → EARN → GROW → SUPPORT**

---

## 📋 About

This is the **Care Partner Operating System** — a complete app that helps Care Partners:

- View their daily workday and duty
- Mark attendance (check-in / check-out)
- Apply for leave
- Access care tasks
- Track earnings and salary
- Learn through training modules
- Grow with performance tracking
- Get support when needed

---

## 🛠️ Technology Stack

**Backend:**
- Python 3.14+
- FastAPI
- PostgreSQL / MySQL (existing Remzy system)
- SQLAlchemy
- JWT Authentication
- Argon2 Password Hashing

**Frontend:**
- React 19
- Vite
- Tailwind CSS
- Axios
- React Router

---

## 📁 Project Structure

remzy-app/
├── backend/
│   └── app/
│       ├── config.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── services.py
│       ├── routes.py
│       ├── main.py
│       └── utils/
│           ├── security.py
│           └── deps.py
└── frontend/
    └── src/
        ├── App.jsx
        ├── main.jsx
        └── pages/
            ├── Attendance.jsx
            └── Leave.jsx

---

## 🚀 Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-jose passlib[argon2] python-dotenv
uvicorn app.main:app --reloadcd frontend
npm install
npm run dev
